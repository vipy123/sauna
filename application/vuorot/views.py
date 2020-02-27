from application import app, db
from flask import render_template, request, url_for, escape, redirect
from flask_login import current_user
from application import login_required
import datetime
from datetime import timedelta
import calendar
from decimal import *
from application.vuorot.models import Sauna, Vuoro
from application.auth.models import Kayttaja, saunaadmin
from application.vuorot.forms import SaunaForm, SaunaUpdateForm, VuoroForm

from sqlalchemy.sql import text

@app.route("/saunat/", methods=["GET"])
def sauna_index():

	return render_template("saunat/saunat.html", saunat=Sauna.query.all())

@app.route("/saunat/new/")
@login_required(role="ADMIN")
def sauna_form():
	return render_template("saunat/new.html", form = SaunaForm())

@app.route("/saunat/new/", methods=["POST"])
@login_required(role="ADMIN")
def tallenna_sauna():
	form = SaunaForm(request.form)
	if not form.validate():
		return render_template("saunat/new.html", form=form)
	sauna = Sauna(form.name.data, form.address.data)
	sauna.hourly_price = form.hourly_price.data
	db.session().add(sauna)
	db.session().commit()
	sauna = Sauna.query.filter_by(name=form.name.data).first()
	sauna.admins.append(current_user)
	
	db.session().commit()
	
	return redirect(url_for("sauna_index"))

@app.route("/saunat/<id>", methods=["GET"])
def sauna_id(id):
	authtext=""
	sauna = Sauna.query.get(id)
	timen = datetime.datetime.now(datetime.timezone(timedelta(hours=2)))
	admins = sauna.admins
	sauna_past_tulot =0.0
	
	sauna_future_tulot =""
	
	if current_user in sauna.admins:
		sauna_past_tulot =sauna.get_sauna_past_tulot(sauna)
		sauna_future_tulot = sauna.get_sauna_future_tulot(sauna)

	return render_template("saunat/sauna.html", sauna=sauna, vuorot=sauna.vuorot,
	timen=timen, admins=admins, authtext=authtext, past_tulot=sauna_past_tulot, future_tulot = sauna_future_tulot)


@app.route("/saunat/<id>/update", methods=["GET"])
@login_required(role="ADMIN")
def sauna_update(id):
	authtext = "Vain saunan hallinnoijat voivat muokata saunan tietoja."
	sauna = Sauna.query.get(id)
	
	admins = sauna.admins
	id = sauna.id
	
	if current_user in admins:
		choices = [ (k.id, k.username) for k in Kayttaja.query.all() ]
		form = SaunaUpdateForm()
		form.name.data=sauna.name
		form.address.data = sauna.address
		form.newadmin.choices = choices
		form.hourly_price.data = sauna.hourly_price

		return render_template("saunat/updateSauna.html", form=form, sauna=sauna)

	else:
		return redirect(url_for("sauna_index"))

@app.route("/saunat/<id>/update", methods=["POST"])
@login_required(role="ADMIN")
def sauna_updateInfo(id):
	authtext =""
	form = SaunaUpdateForm(request.form)
	name = form.name.data
	address = form.address.data
	sauna = Sauna.query.get(id)
	sauna.name = name
	sauna.address = address
	newadminid = form.newadmin.data
	newadmin = Kayttaja.query.get(newadminid)
	sauna.hourly_price = form.hourly_price.data
	if newadminid != current_user.id:
		sauna.admins.append(newadmin)

	db.session().commit()

	return redirect(url_for("sauna_id", id = sauna.id))

@app.route("/saunat/delete/<id>", methods=["POST"])
@login_required(role="ADMIN")
def sauna_delete(id):
	sauna = Sauna.query.get(id)
	if current_user in sauna.admins:
		for vuoro in sauna.vuorot:
			db.session.delete(vuoro)
		current_user.saunat.remove(sauna)
		for admin in sauna.admins:
			sauna.admins.remove(admin)
		
		db.session.delete(sauna)
		db.session.commit()

	return redirect(url_for("sauna_index"))

@app.route("/saunat/<id>/newvuoro", methods=["GET"])
@login_required(role="ADMIN")
def new_vuoro(id):
	sauna = Sauna.query.get(id)
	if current_user in sauna.admins:
		return render_template("vuorot/new_vuoro.html", form=VuoroForm(), id=id)
	else:
		return redirect(url_for("sauna_id", id = sauna.id))

@app.route("/saunat/<id>/newvuoro", methods=["POST"])
@login_required(role="ADMIN")
def add_new_vuoro(id):
	form = VuoroForm(request.form)
	
	reserver_id=current_user.id
	sauna_id=id
	sauna = Sauna.query.get(id)
	date = form.datef.data
	time_start = form.timestartf.data
	time_start_dt = datetime.datetime.combine(datetime.datetime(1,1,1,0,0,0), time_start)
	time_end= form.timeendf.data
	time_end_dt = datetime.datetime.combine(datetime.datetime(1,1,1,0,0,0), time_end)
	var = form.varattu.data
	timedelta = time_end_dt - time_start_dt
	time_decimal = timedelta.total_seconds()/3600
	vuoro = Vuoro(reserver_id, sauna_id, date, time_start, time_end, var)
	vuoro.price = sauna.hourly_price * Decimal(time_decimal)
	db.session().add(vuoro)
	db.session().commit()
	return redirect(url_for("sauna_id", id=id))

@app.route("/vuorot/<id>", methods=["GET"])
@login_required
def vuoro_id(id):
	 
	vuoro = Vuoro.query.get(id)
	form = VuoroForm(request.form)
	
	sauna_id=id
	form.datef.data = vuoro.date
	form.timestartf.data = vuoro.time_start
	form.timeendf.data = vuoro.time_end
	form.varattu.data = vuoro.varattu

	return render_template("vuorot/vuoro.html", vuoro=vuoro, form=form)

@app.route("/vuorot/<id>", methods=["POST"])
@login_required
def vuoro_update(id):
	vuoro = Vuoro.query.get(id)
	form = VuoroForm(request.form)
	
	reserver_id=current_user.id
	sauna_id=id
	vuoro.date= form.datef.data
	vuoro.time_start = form.timestartf.data
	vuoro.time_end = form.timeendf.data
	vuoro.varattu = form.varattu.data
	time_start_dt = datetime.datetime.combine(datetime.datetime(1,1,1,0,0,0), vuoro.time_start)
	time_end_dt = datetime.datetime.combine(datetime.datetime(1,1,1,0,0,0), vuoro.time_end)
	timedelta = time_end_dt - time_start_dt
	time_decimal = timedelta.total_seconds()/3600
	sauna = Sauna.query.get(vuoro.sauna_id)
	vuoro.price = sauna.hourly_price * Decimal(time_decimal)
	db.session().commit()
	
	return redirect(url_for("sauna_id", id=sauna.id))

@app.route("/vuorot/<id>/delete", methods=["POST"])
@login_required
def vuoro_delete(id):
	vuoro = Vuoro.query.get(id)
	sauna_id = vuoro.sauna_id
	db.session.delete(vuoro)
	db.session.commit()
	return redirect(url_for("sauna_id", id=sauna_id))
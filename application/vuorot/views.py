from application import app, db
from flask import render_template, request, url_for, escape, redirect
from flask_login import current_user
from application import login_required
import datetime
from datetime import timedelta
import calendar

from application.vuorot.models import Sauna, Vuoro
from application.vuorot.forms import SaunaForm, SaunaUpdateForm, VuoroForm

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
	s = Sauna(form.name.data, form.address.data)
	s.admin_id = current_user.id

	db.session().add(s)
	db.session().commit()
	
	return redirect("/saunat/")

@app.route("/saunat/<id>", methods=["GET"])
def sauna_id(id):
	sauna = Sauna.query.get(id)
	timen = datetime.datetime.now(datetime.timezone(timedelta(hours=2)))
	print(f'VARATUT VUOROT: {sauna.vuorot}')
	return render_template("saunat/sauna.html", sauna=sauna, vuorot=sauna.vuorot, timen=timen)


@app.route("/saunat/<id>/update", methods=["GET"])
@login_required
def sauna_update(id):
	s = Sauna.query.get(id)
	if s.admin_id == current_user.id:
		form = SaunaUpdateForm()
		form.name.data=s.name
		form.address.data = s.address

		return render_template("saunat/updateSauna.html", form=form, sauna=s)

	else:
		return redirect(url_for("sauna_id"), id=id)

@app.route("/saunat/<id>/update", methods=["POST"])
@login_required
def sauna_updateInfo(id):
	form = SaunaUpdateForm(request.form)
	name = request.form.get("name")
	address=request.form.get("address")
	sauna = Sauna.query.get(id)
	sauna.name = name
	sauna.address = address
	db.session().commit()

	return redirect(url_for("sauna_id", id=id))

@app.route("/saunat/delete/<id>", methods=["POST"])
@login_required
def sauna_delete(id):
    sauna = Sauna.query.get(id)
    db.session.delete(sauna)
    db.session.commit()

    return redirect(url_for("sauna_index"))

@app.route("/saunat/<id>/newvuoro", methods=["GET"])
@login_required
def new_vuoro(id):
	return render_template("vuorot/new_vuoro.html", form=VuoroForm(), id=id)

@app.route("/saunat/<id>/newvuoro", methods=["POST"])
@login_required
def add_new_vuoro(id):
	form = VuoroForm(request.form)
	
	reserver_id=current_user.id
	sauna_id=id
	date = form.datef.data
	time_start = form.timestartf.data
	time_end= form.timeendf.data
	var = form.varattu.data
	v = Vuoro(reserver_id, sauna_id, date, time_start, time_end, var)
	db.session().add(v)
	db.session().commit()
	return redirect(url_for("sauna_index"))

@app.route("/vuorot/<id>", methods=["GET"])
@login_required
def vuoro_id(id):
	vuoro = Vuoro.query.get(id)
	return render_template("vuorot/vuoro.html", vuoro=vuoro)

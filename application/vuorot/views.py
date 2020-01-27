from application import app, db
from flask import render_template, request, url_for, escape, redirect
from application.vuorot.models import Sauna
from application.vuorot.forms import SaunaForm, SaunaUpdateForm

@app.route("/saunat/", methods=["GET"])
def sauna_index():
	saunat = Sauna.query.all()

	return render_template("saunat/saunat.html", saunat=Sauna.query.all())

@app.route("/saunat/new/")
def sauna_form():
	return render_template("saunat/new.html", form = SaunaForm())

@app.route("/saunat/new/", methods=["POST"])
def tallenna_sauna():
	form = SaunaForm(request.form)
	if not form.validate():
		return render_template("saunat/new.html", form=form)
	s = Sauna(form.name.data, form.address.data)
	db.session().add(s)
	db.session().commit()
	
	return redirect("/saunat/")

@app.route("/saunat/<id>", methods=["GET"])
def sauna_id(id):
	sauna = Sauna.query.get(id)
	
	return render_template("saunat/sauna.html", sauna=sauna)


@app.route("/saunat/<id>/update", methods=["GET"])
def sauna_update(id):
	s = Sauna.query.get(id)
	form = SaunaUpdateForm()
	form.name.data=s.name
	form.address.data = s.address

	return render_template("saunat/updateSauna.html", form=form, sauna=s)

@app.route("/saunat/<id>/update", methods=["POST"])
def sauna_updateInfo(id):
	form = SaunaUpdateForm(request.form)
	name = request.form.get("name")
	address=request.form.get("address")
	sauna = Sauna.query.get(id)
	sauna.name = name
	sauna.address = address
	db.session().commit()

	return redirect(url_for("sauna_id", id=id))


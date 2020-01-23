from application import app, db
from flask import render_template, request, url_for, escape
from application.vuorot.models import Sauna, Kayttaja

@app.route("/saunat/", methods=["GET"])
def sauna_index():
	saunat = Sauna.query.all()

	return render_template("saunat/saunat.html", saunat=Sauna.query.all())

@app.route("/saunat/new/")
def sauna_form():
	return render_template("saunat/new.html")

@app.route("/saunat/new/", methods=["POST"])
def tallenna_sauna():
	s = Sauna(name=request.form.get("name"), address=request.form.get("address"))
	db.session().add(s)
	db.session().commit()
	
	return "Sauna on tallennettu!"

@app.route("/saunat/<id>", methods=["GET", "POST"])
def sauna_id(id):
	sauna = Sauna.query.get(id)
	
	return render_template("saunat/sauna.html", sauna=sauna)

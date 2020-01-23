from application import app, db
from flask import render_template, request
from application.vuorot.models import Sauna, Kayttaja

@app.route("/saunat/", methods=["GET"])
def sauna_index():
	return render_template("saunat/saunat.html", saunat = Sauna.query.all())

@app.route("/saunat/new/")
def sauna_form():
	return render_template("saunat/new.html")

@app.route("/saunat/new/", methods=["POST"])
def tallenna_sauna():
	s = Sauna(name=request.form.get("name"), address=request.form.get("address"))
	db.session().add(s)
	db.session().commit()
	
	return "Sauna on tallennettu!"

@app.route("/saunat/<sauna_id>", methods=["GET"])
def sauna_index():
	return render_template("saunat/sauna.html", sauna = #Sauna.query.all())

from application import app
from flask import render_template, request
from application.vuorot.models import Kayttaja

@app.route("/kayttajat/new/")
def kayttaja_form():
	return render_template("kayttajat/new.html")

@app.route("/kayttajat/", method=["POST"])
def tallenna_kayttaja():
	u = Kayttaja(name=request.form.get("name"), address=name=request.form.get("address"))
	db.session().add(u)
	db.session().commit()
	
	return "Käyttajätunnuksesi on tallennettu!"

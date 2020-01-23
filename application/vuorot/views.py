from application import app
from flask import render_template, request

@app.route("/kayttajat/new/")
def kayttaja_form():
	return render_template("kayttajat/new.html")

@app.route("/kayttajat/", method=["POST"])
def tallenna_kayttaja():
	print(request.form.get("name"))
	return "Käyttajätunnuksesi on tallennettu!"

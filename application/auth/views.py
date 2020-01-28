from application import app, db
from flask import render_template, request, url_for, escape, redirect
from flask_login import login_user
from application.auth.models import Kayttaja
from application.auth.forms import LoginForm

@app.route("/auth/login", methods=["GET", "POST"])
def auth_login():
	if request.method == "GET":
		return render_template("auth/loginform.html", form = LoginForm())
	
	form = LoginForm(request.form)
	
	kayttaja = Kayttaja.query.filter_by(username=form.username.data, password=form.password.data).first()
	if not kayttaja:
		return render_template("auth/loginform.html", form=form, error="Käyttäjää ei löydy")
	print("Käyttäjä " + kayttaja.username + " tunnistettiin")
	login_user(kayttaja)

	return redirect(url_for("sauna_index"))




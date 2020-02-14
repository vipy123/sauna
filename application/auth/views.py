from application import app, db
from flask import render_template, request, url_for, escape, redirect
from flask_login import login_user, logout_user
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

@app.route("/auth/logout")
def auth_logout():
	logout_user()
	return redirect(url_for("index"))

@app.route("/auth/register", methods=["GET", "POST"])
def auth_register():
	if request.method == "GET":
		return render_template("auth/signup.html", form = SigUpForm)
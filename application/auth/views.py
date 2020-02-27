from application import app, db
from flask import render_template, request, url_for, escape, redirect
from flask_login import login_user, logout_user, current_user
from application.auth.models import Kayttaja
from application.vuorot.models import Sauna, Vuoro
from application.auth.forms import LoginForm, SignUpForm
from application import app, db, login_required


@app.route("/auth/login", methods=["GET", "POST"])
def auth_login():
    if request.method == "GET":
        return render_template("auth/loginform.html", form=LoginForm())

    form = LoginForm(request.form)

    kayttaja = Kayttaja.query.filter_by(
        username=form.username.data, password=form.password.data).first()
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
        return render_template("auth/signup.html", form=SignUpForm())
    else:
        form = SignUpForm(request.form)
        username = form.username.data
        name = form.name.data
        phonenumber = form.phonenumber.data
        address = form.address.data
        rolebox = form.rolebox.data
        if rolebox:
            roles = "ADMIN"
        else:
            roles = "USER"
        password = form.password.data
        kayttaja = Kayttaja(username, name, phonenumber, address, password, roles)
    
        db.session().add(kayttaja)
        db.session().commit()
        return redirect(url_for("auth_login"))

@app.route("/auth/kayttaja/<id>", methods=["GET"])
@login_required()
def auth_kayttaja(id):
    yhteenveto_kayttajan_saunoista = current_user.saunat_joihin_varauksia(current_user.id)
    saunavarausten_maara = current_user.saunavarausten_maara(current_user.id)
    tulotsaunoista = 0.0
    show= False
    if current_user.roles=='ADMIN':
        show = True

    tulotsaunoista = current_user.tulot_saunoista(id)

    return render_template("auth/kayttaja.html", yhteenveto_kayttajan_saunoista=yhteenveto_kayttajan_saunoista, show=show, maara=saunavarausten_maara, tulot=tulotsaunoista)

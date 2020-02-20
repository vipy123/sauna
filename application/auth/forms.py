from flask_wtf import FlaskForm
from wtforms import Form, PasswordField, StringField, BooleanField, validators
from wtforms.validators import InputRequired, Email, Length, DataRequired, EqualTo


class LoginForm(FlaskForm):
    username = StringField("Käyttäjätunnus")
    password = PasswordField("Salasana")

    class Meta:
        csrf = False


class SignUpForm(FlaskForm):
    name = StringField("Etunimi sukunimi", [validators.Length(min=5, max=144)])
    username = StringField(
        "Käyttäjätunnus", [validators.Length(min=2, max=15)])
    phonenumber = StringField(
        "Puhelinnumero", [validators.Length(min=2, max=20)])
    address = StringField("Osoite", [validators.Length(min=2, max=144)])
    rolebox = BooleanField("Oletko saunan hallitsija tai isännöitsijä")
    password = PasswordField("Salasana", [
        validators.Length(min=6, max=144),
        validators.DataRequired(),
        validators.EqualTo('password2', message='Password must match')])
    password2 = PasswordField("Salasana uudestaan")

    class Meta:
        csrf = False

from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, BooleanField
from wtforms.validators import InputRequired, Email, Length

class LoginForm(FlaskForm):
	username = StringField("Käyttäjätunnus")
	password = PasswordField("Salasana")

	class Meta:
		csrf = False

class SignUpForm(FlaskForm):
	name = StringField("Etunimi sukunimi")
	username = StringField("Käyttäjätunnus")
	phonenumber = StringField("Puhelinnumero")
	password = PasswordField("Salasana")
	password = PasswordField("Salasana uudestaan")
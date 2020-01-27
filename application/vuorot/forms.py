from flask_wtf import FlaskForm
from wtforms import StringField, validators
from application.vuorot.models import Sauna

class SaunaForm(FlaskForm):
	name = StringField("Saunan nimi", [validators.Length(min=2, max=144)])
	address = StringField("Saunan osoite", [validators.Length(min=5, max=144)])
	class Meta:
		csrf = False

class SaunaUpdateForm(FlaskForm):
	
	name = StringField("Saunan nimi")
	address = StringField("Saunan osoite")
	class Meta:
		csrf = False

from flask_wtf import FlaskForm
from wtforms import StringField, validators, TimeField, BooleanField, SelectField
from application.vuorot.models import Sauna
from wtforms.fields.html5 import DateField

class SaunaForm(FlaskForm):
	name = StringField("Saunan nimi", [validators.Length(min=2, max=144)])
	address = StringField("Saunan osoite", [validators.Length(min=5, max=144)])
	class Meta:
		csrf = False

class SaunaUpdateForm(FlaskForm):
	
	name = StringField("Saunan nimi", [validators.Length(min=2, max=144)])
	address = StringField("Saunan osoite", [validators.Length(min=5, max=144)])
	newadmin = SelectField("Lisää uusi hallinnoija saunalle (nimi)")
	class Meta:
		csrf = False
		
class VuoroForm(FlaskForm):
	datef = DateField("Päivämäärä: DD.MM.YYYY")
	timestartf = TimeField("Aloitusaika: HH:MM", format='%H:%M')
	timeendf = TimeField("Lopetusaika: HH:MM", format='%H:%M')
	varattu = BooleanField("Imoitetaan varatuksi", False)

	class Meta:
		csrf = False

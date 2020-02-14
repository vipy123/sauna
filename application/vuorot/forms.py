from flask_wtf import FlaskForm
from wtforms import StringField, validators, DateField, TimeField, BooleanField
from application.vuorot.models import Sauna

class SaunaForm(FlaskForm):
	name = StringField("Saunan nimi", [validators.Length(min=2, max=144)])
	address = StringField("Saunan osoite", [validators.Length(min=5, max=144)])
	class Meta:
		csrf = False

class SaunaUpdateForm(FlaskForm):
	
	name = StringField("Saunan nimi", [validators.Length(min=2, max=144)])
	address = StringField("Saunan osoite", [validators.Length(min=5, max=144)])
	class Meta:
		csrf = False
		
class VuoroForm(FlaskForm):
	datef = DateField("Päivämäärä: DD.MM.YYYY", format='%d.%m.%Y')
	timestartf = TimeField("Aloitusaika: HH:MM", format='%H:%M')
	timeendf = TimeField("Lopetusaika: HH:MM", format='%H:%M')
	varattu = BooleanField("Imoitetaan varatuksi", False)

	class Meta:
		csrf = False

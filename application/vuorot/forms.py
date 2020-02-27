from flask_wtf import FlaskForm
from wtforms import StringField, validators, TimeField, BooleanField, SelectField, DecimalField
from application.vuorot.models import Sauna
from wtforms.fields.html5 import DateField

class SaunaForm(FlaskForm):
	name = StringField("Saunan nimi", [validators.Length(min=2, max=20, message="Nimen tulee olla vähintään 2 ja enintään 20 merkkiä pitkä")])
	address = StringField("Saunan osoite", [validators.Length(min=5, max=30, message="Osoitteen tulee olla vähintään 5 ja enintään 30 merkkiä pitkä")])
	hourly_price = DecimalField("Lisää saunan tuntihinta", [validators.NumberRange(min=0, max=300, message="Tuntihinnan tulee olla positiivinen desimaaliluku 0-300")])
	class Meta:
		csrf = False

class SaunaUpdateForm(FlaskForm):
	
	name = StringField("Saunan nimi", [validators.Length(min=2, max=20, message="Nimen tulee olla vähintään 2 ja enintään 20 merkkiä pitkä")])
	address = StringField("Saunan osoite", [validators.Length(min=5, max=30, message="Osoitteen tulee olla vähintään 5 ja enintään 30 merkkiä pitkä")])
	newadmin = SelectField("Lisää uusi hallinnoija saunalle (nimi)")
	hourly_price = DecimalField("Lisää saunan tuntihinta", [validators.NumberRange(min=0, max=300, message="Tuntihinnan tulee olla positiivinen desimaaliluku pisteellä erotettuna (.) 0.0-300.00")])
	class Meta:
		csrf = False
		
class VuoroForm(FlaskForm):
	datef = DateField("Päivämäärä: ")
	timestartf = TimeField("Aloitusaika: HH:MM", format='%H:%M')
	timeendf = TimeField("Lopetusaika: HH:MM", format='%H:%M')
	varattu = BooleanField("Imoitetaan varatuksi", False)

	class Meta:
		csrf = False

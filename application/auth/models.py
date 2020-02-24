from application import db
from sqlalchemy.sql import text
from sqlalchemy.orm import relationship, backref
from flask_login import current_user

saunaKayttaja = db.Table('SaunaKayttaja', 
		db.Column('kayttaja_id', db.Integer, db.ForeignKey('kayttaja.id')),
		db.Column('sauna_id', db.Integer, db.ForeignKey('sauna.id')))

class Kayttaja(db.Model):
	
	id = db.Column(db.Integer, primary_key=True)
	date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
	date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),
							  onupdate=db.func.current_timestamp())
	username = db.Column(db.String(144), nullable=False)
	name = db.Column(db.String(144), nullable=False)
	address = db.Column(db.String(200), nullable=True)
	password = db.Column(db.String(144), nullable=False)
	email = db.Column(db.String(144))
	phonenumber = db.Column(db.String(20))
	vuorot = db.relationship("Vuoro", backref='reserver', lazy=True)
	saunat = db.relationship("Sauna", secondary=saunaKayttaja, backref=db.backref('Kayttaja', lazy='dynamic'))
	roles = db.Column(db.String(10), nullable=False)


	def __init__(self, username, name, phonenumber, address, password, roles):
		self.username = username
		self.name = name
		self.phonenumber = phonenumber
		self.address = address
		self.password = password
		self.roles = roles

	def get_id(self):
		return self.id

	def is_active(self):
		return True

	def is_anonymous(self):
		return False

	def is_authenticated(self):
		return True

	def roles(self):
		return roles

	@staticmethod
	def saunat_joihin_varauksia(k_id):
		stmt = text('SELECT DISTINCT name FROM Sauna LEFT JOIN Vuoro ON Sauna.id = Vuoro.sauna_id WHERE Vuoro.reserver_id = :kid').params(kid = k_id)
		countstmt = text('SELECT COUNT(DISTINCT name) FROM Sauna LEFT JOIN Vuoro ON Sauna.id = Vuoro.sauna_id WHERE Vuoro.reserver_id = :kid').params(kid = k_id)
		count = db.engine.execute(countstmt)
		res = db.engine.execute(stmt)
		response = []
		count2= []
		for row in res:
			response.append(row[0])
		for row in count:
			count2.append(row[0])

		return 'Hei ', current_user.name, '! Sinulla on varauksia ', count2[0], ' saunaan: ', response
		


"""Alla oleva luokka muutettiin sivun ylälaidassa olevaksi liitostauluksi, koska halutttiin yksinkertaistaa ohjelmaa."""

""" class SaunaKayttaja(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	sauna_id = db.Column(db.Integer, db.ForeignKey('sauna.id'), nullable=False)
	kayttaja_id = db.Column(db.Integer, db.ForeignKey('kayttaja.id'), nullable=False)

	sauna = db.relationship(Sauna, backref="SaunaKayttaja")
	kayttaja = db.relationship(Kayttaja, backref="SaunaKayttaja")

	def __init__(self, sauna_id, kayttaja_id):
		self.sauna_id = sauna_id
		self.kayttaja_id = kayttaja_id """

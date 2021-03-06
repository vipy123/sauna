from application import db
from sqlalchemy.sql import text
from sqlalchemy.orm import relationship, backref
from flask_login import current_user



saunaadmin = db.Table("saunaadmin",
		db.Column("kayttaja_id", db.Integer, db.ForeignKey("kayttaja.id")),
		db.Column("sauna_id", db.Integer, db.ForeignKey("sauna.id")))

class Kayttaja(db.Model):
	__tablename__="kayttaja"
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

	saunat = db.relationship("Sauna", secondary=saunaadmin, cascade="all,delete", back_populates='admins')
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
	def saunat_joihin_varauksia(kayttaja_id):
		stmt = text('SELECT DISTINCT name FROM sauna LEFT JOIN vuoro ON sauna.id = vuoro.sauna_id WHERE vuoro.reserver_id = :kayttajaid').params(kayttajaid = kayttaja_id)
		
		res = db.engine.execute(stmt)
		response = []
		
		for row in res:
			response.append(row[0])

		return response

	@staticmethod
	def saunavarausten_maara(kayttaja_id):
		
		countstmt = text('SELECT COUNT(DISTINCT name) FROM sauna LEFT JOIN vuoro ON sauna.id = vuoro.sauna_id WHERE vuoro.reserver_id = :kayttajaid').params(kayttajaid = kayttaja_id)
		count = db.engine.execute(countstmt)
		
		count2= []
		
		for row in count:
			count2.append(row[0])

		return count2[0]

	@staticmethod
	def tulot_saunoista(kayttaja_id):
		stmt = text("SELECT SUM(price) FROM Vuoro LEFT JOIN Sauna ON Vuoro.sauna_id = Sauna.id LEFT JOIN saunaadmin ON Sauna.id = saunaadmin.sauna_id WHERE saunaadmin.kayttaja_id = :kayttaja_id AND Vuoro.date < CURRENT_DATE AND Vuoro.varattu ='1'").params(kayttaja_id = kayttaja_id)
		res = db.engine.execute(stmt)
		response = []
		
		for row in res:
			response.append(row[0])

		return response[0]

	

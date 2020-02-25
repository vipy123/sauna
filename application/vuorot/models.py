from application import db
from application.auth.models import Kayttaja, saunaadmin
from sqlalchemy.sql import text
from sqlalchemy.orm import relationship, backref


class Sauna(db.Model):
	__tablename__="sauna"
	id = db.Column(db.Integer, primary_key=True)
	date_created = db.Column(db.Date)
	date_current = db.Column(db.Date, default=db.func.current_timestamp())

	name = db.Column(db.String(144), nullable=False)
	address = db.Column(db.String(200), nullable=False)
	admins = db.relationship("Kayttaja", secondary=saunaadmin, back_populates='saunat')
	#hourly_price = db.Column(db.Float)
	vuorot = db.relationship("Vuoro", backref='Sauna', lazy=True)

	def __init__(self, name, address):
		self.name = name
		self.address = address
	
	@staticmethod
	def show_future_vuorot(id):
		stmt = text("SELECT * FROM vuoro WHERE sauna_id = :id AND date > CURRENT_TIME").params(id=id)
		res = db.engine.execute(stmt)
		response = []
		for row in res:
			response.append({row[0]})
		return response

	@staticmethod
	def is_sauna_admin(self, kayttajan_id):
		stmt = text("SELECT kayttaja_id FROM saunaadmin WHERE sauna_id = :sid AND kayttaja_id = :kayttajan_id").params(sid=self.id, kayttajan_id=kayttajan_id)
		res = db.engine.execute(stmt)
		response = []
		for row in res:
			response.append({row[0]})
		if kayttajan_id in response:
			return True
		else:
			return False


class Vuoro(db.Model):
	__tablename__="vuoro"
	id = db.Column(db.Integer, primary_key=True)
	reserver_id = db.Column(db.Integer, db.ForeignKey("kayttaja.id"), nullable=False)
	#reserver = db.relationship("Kayttaja", backref="Vuoro")
	sauna_id = db.Column(db.Integer, db.ForeignKey("sauna.id"), nullable=False)
	sauna = db.relationship("Sauna", backref="Vuoro", lazy=True)
	date = db.Column(db.Date, nullable=False)
	time_start = db.Column(db.Time, nullable=False)
	time_end = db.Column(db.Time, nullable=False)
	varattu = db.Column(db.Boolean)
	#price = db.Column(db.Numeric((time_end - time_start)*2))
	def __init__(self, reserver_id, sauna_id, date,  time_start, time_end, varattu):
		self.reserver_id = reserver_id
		self.sauna_id = sauna_id
		self.date = date
		self.time_start = time_start
		self.time_end = time_end
		self.varattu = varattu

	def get_id(self):
		return self.id



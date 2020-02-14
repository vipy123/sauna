from application import db
from application.auth.models import Kayttaja
#from sqlalchemy.orm import backref


class Sauna(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	date_created = db.Column(db.DateTime)
	date_current = db.Column(db.DateTime, default=db.func.current_timestamp())

	name = db.Column(db.String(144), nullable=False)
	address = db.Column(db.String(200), nullable=False)
	admin_id = db.Column(db.Integer, db.ForeignKey('kayttaja.id'), nullable=False)
	hourly_price = db.Column(db.Float)
	vuorot = db.relationship("Vuoro", backref='sauna', lazy=True)

	def __init__(self, name, address):
		self.name = name
		self.address = address
	
	@staticmethod
	def show_future_vuorot(id):
		stmt = text("SELECT * FROM Vuoro WHERE sauna_id = id AND time_start > CURRENT_TIME").params(id=id)



class Vuoro(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	reserver_id = db.Column(db.Integer, db.ForeignKey('kayttaja.id'), nullable=False)
	sauna_id = db.Column(db.Integer, db.ForeignKey('sauna.id'), nullable=False)
	
	time_start = db.Column(db.DateTime, nullable=False)
	time_end = db.Column(db.DateTime, nullable=False)
	varattu = db.Column(db.Boolean)
	#price = db.Column(db.Float((time_end - time_start)*2))
#	def __init__(self, reserver_id, sauna_id, time_start, time_end, varattu):
#		self.reserver_id = reserver_id
#		self.sauna_id = sauna_id
#		self.time_start = time_start
#		self.time_end = time_end
#		self.varattu = varattu

	def __init__(self, reserver_id, sauna_id, time_start, varattu):
		self.reserver_id = reserver_id
		self.sauna_id = sauna_id
		self.time_start = time_start
		self.varattu = varattu

	def get_id(self):
		return self.id



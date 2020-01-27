from application import db

class Sauna(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
	date_current = db.Column(db.DateTime)

	name = db.Column(db.String(144), nullable=False)
	address = db.Column(db.String(200), nullable=False)
	admin_id = db.Column(db.Integer)

	def __init__(self, name, address):
		self.name = name
		self.address = address
		

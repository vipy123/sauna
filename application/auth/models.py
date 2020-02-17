from application import db
from application.vuorot import models


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
    saunat = db.relationship("SaunaKayttaja", backref='admin', lazy=True)

    def __init__(self, username, name, phonenumber, address, password):
        self.username = username
        self.name = name
        self.phonenumber = phonenumber
        self.address = address
        self.password = password

    def get_id(self):
        return self.id

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return True

    def roles(self):
        return ["ADMIN"]

class SaunaKayttaja(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	sauna_id = db.Column(db.Integer, db.ForeignKey('sauna.id'), nullable=False)
	kayttaja_id = db.Column(db.Integer, db.ForeignKey('kayttaja.id'), nullable=False)

	def __init__(self, sauna_id, kayttaja_id):
		self.sauna_id = sauna_id
		self.kayttaja_id = kayttaja_id
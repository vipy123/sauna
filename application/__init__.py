from flask import Flask

from flask_sqlalchemy import SQLAlchemy
import os
from os import urandom

from functools import wraps

app = Flask(__name__)

if os.environ.get("HEROKU"):
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
else:
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///vuorot.db"
    app.config["SQLALCHEMY_ECHO"] = True

db = SQLAlchemy(app)

app.config["SECRET_KEY"] = urandom(32)

from flask_login import LoginManager, current_user

login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = "auth_login"
login_manager.login_message = "Please login to use this functionality."


# roles in login_required
def login_required(_func=None, *, role="ANY"):
    def wrapper(func):
        @wraps(func)
        def decorated_view(*args, **kwargs):
            if not (current_user and current_user.is_authenticated):
                return login_manager.unauthorized()

            acceptable_roles = set(("ANY", "ADMIN", "USER"))
            if role not in acceptable_roles:
                return login_manager.unauthorized()
            return func(*args, **kwargs)
        return decorated_view
    return wrapper if _func is None else wrapper(_func)

from application import views
from application.vuorot import models
from application.vuorot import views
from application.auth import models
from application.auth import views

from application.auth.models import Kayttaja

@login_manager.user_loader
def load_user(kayttaja_id):
    return Kayttaja.query.get(kayttaja_id)


try:
    db.create_all()
except:
    pass

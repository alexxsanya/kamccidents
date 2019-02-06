from flask import Flask
from models import db, bcrypt
import config
from os import environ 
from flask_bootstrap import Bootstrap

def init_app():
    app = Flask(__name__) 
    app.config.from_object(environ['APP_SETTINGS'])
    Bootstrap(app)
    bcrypt.init_app(app)
    db.init_app(app) 
    return app
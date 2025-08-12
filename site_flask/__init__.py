from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///banco.db'
#os.getenv('DATABASE_URL','sqlite:///banco.db').replace('postegres://','postegresql://')

app.config['SECRET_KEY']='b2c8707d67548b2df213a261d90cf531f4f1d02e'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"

    
import site_flask.routes as routes
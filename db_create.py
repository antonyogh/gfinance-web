from site_flask.models import Gasto,Conta,Usuario
from site_flask import app,db

with app.app_context():
    db.create_all()
from site_flask import db,login_manager,app
from sqlalchemy import Column,String,Integer,Float
from datetime import datetime
from flask_login import UserMixin

@login_manager.user_loader
def load_usuario(id):
    return Usuario.query.get(int(id))

class Usuario(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key=True)
    usuario = db.Column(db.String,nullable=False)
    senha = db.Column(db.String,nullable=False)
    conta = db.relationship('Conta',backref='usuario',lazy=True)
    gasto = db.relationship('Gasto',backref='usuario',lazy=True)
    despesa = db.relationship('Receita',backref='usuario',lazy=True)

class Conta(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    saldo = db.Column(db.Float,nullable=False)
    id_usuario = db.Column(db.Integer,db.ForeignKey('usuario.id'),nullable=False)
    
class Gasto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String,nullable=False)
    valor = db.Column(db.Float,nullable=False)
    categoria = db.Column(db.String,default='Nenhuma')
    data = db.Column(db.String,default=datetime.strftime(datetime.now(),'%d/%m/%Y'))
    id_usuario = db.Column(db.Integer,db.ForeignKey('usuario.id'),nullable=False)

class Receita(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    fonte = db.Column(db.String,nullable=False)
    valor = db.Column(db.Float,nullable=False)
    data = db.Column(db.String,default=datetime.strftime(datetime.now(),'%d/%m/%Y'))
    id_usuario = db.Column(db.Integer,db.ForeignKey('usuario.id'),nullable=False)

#with app.app_context():
 #   db.create_all()
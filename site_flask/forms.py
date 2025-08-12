from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,DecimalField,\
    FloatField,SelectField,Label,DateTimeField,DateTimeLocalField
from wtforms.validators import DataRequired,ValidationError,EqualTo,Length
from datetime import datetime

class FormLogin(FlaskForm):
    usuario = StringField('Usuário',validators=[DataRequired()])
    senha = PasswordField('Senha',validators=[DataRequired()])
    btlogin = SubmitField('Entrar')
    msg = Label('msg',text='')

class FormCriarConta(FlaskForm):
    usuario = StringField('Usuário',validators=[DataRequired()])
    senha = PasswordField('Senha',validators=[DataRequired(),Length(6,16)])
    confirma_senha = PasswordField('Confirmar senha',validators=[DataRequired(),EqualTo('senha')])
    btcriar = SubmitField('Criar conta')

class FormContaConfig(FlaskForm):
    saldo = FloatField('Saldo',validators=[DataRequired()],default=0.0)
    btsalvar = SubmitField('Salvar')

class ItemList(FlaskForm):
    texto = StringField('Texto')

class FormAddGasto(FlaskForm):
    descricao = StringField('Descrição',validators=[DataRequired()])
    valor = DecimalField('Valor',validators=[DataRequired()])
    input_categoria = StringField("input_ctg")
    categoria = SelectField('Categoria',validate_choice=False)
    btsalvar = SubmitField('Salvar')

class AddReceita(FlaskForm):
    fonte = StringField('Fonte',validators=[DataRequired()])
    valor = FloatField('Valor',validators=[DataRequired()])
    rdata = DateTimeField(default=datetime.strftime(datetime.now(),'%d/%m/%Y'))
    btsalvar = SubmitField('Salvar')

class Periodo(FlaskForm):
    di = SelectField("Periodo")
    df = DateTimeField('Data_Final')



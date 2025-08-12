from flask import render_template,request,redirect,url_for,flash
from flask_login import login_required,login_user,current_user,logout_user
from site_flask import app,db,bcrypt
from site_flask.models import Gasto,Usuario,Conta,Receita
from site_flask.forms import FormCriarConta,FormLogin,FormAddGasto,FormContaConfig,AddReceita,Periodo
from site_flask import gastos_manager,receitas_manager
import plotly.graph_objs as go

#Login
@app.route('/',methods=['GET','POST'])
def login():
    form_login = FormLogin()
    if form_login.validate_on_submit:
        usuario = Usuario.query.filter_by(usuario=form_login.usuario.data).first()
        if usuario and bcrypt.check_password_hash(usuario.senha,form_login.senha.data):
            login_user(usuario)
            return redirect(url_for('home'))
        else:
            flash('Dados inválidos!','message')
    return render_template('login.html',form=form_login)

#Criar conta
@app.route('/criarconta',methods=['GET','POST'])
def criarconta():
    form_criar_conta = FormCriarConta()
    if form_criar_conta.validate_on_submit():
        senha = bcrypt.generate_password_hash(form_criar_conta.senha.data)
        usuario = Usuario(usuario=form_criar_conta.usuario.data,senha=senha)
        db.session.add(usuario)
        db.session.commit()
        login_user(usuario,remember=True)
        return redirect(url_for('perfil',id=usuario.id))
    return render_template('criar_conta.html',form=form_criar_conta)

#Inicio
@app.route('/home',methods=['GET','POST'])
@login_required
def home():
    saldo =0.0
    gastos =  Gasto.query.all()
    vg = 0
    gc = gastos_manager.get_gastos_categoria(gastos)
    if len(current_user.conta)>0:
       saldo =current_user.conta[0].saldo
    if len(gastos)>0:
       vg = gastos_manager.get_valor_total(gastos)

    dados = {'gastos':[],'valor':vg,'usuario':str(current_user.usuario).capitalize()
             ,'saldo':saldo}

    return render_template('home.html', dados=dados)

#Configurar conta
@app.route('/contaconfig',methods=['GET','POST'])
@login_required
def contaconfig():
    form = FormContaConfig()
    conta = None
    if len(current_user.conta)>0:
       conta=current_user.conta[0]
       form.saldo.data=conta.saldo
    else:
        conta =Conta()
    if form.validate_on_submit():
       conta.saldo=FormContaConfig().saldo.data
       conta.id_usuario=int(current_user.id)
       db.session.add(conta)
       db.session.commit()
       return redirect(url_for('home'))
    
    return render_template('conta_config.html',form=form)

#Sobre
@app.route('/sobre', methods=['GET','POST'])
def sobre():
    m =['Jan','Fev','Mar','Abr']
    v =[200,400,520,300]
    fig = go.Figure([go.Bar(x=m,y=v)])
    pie = go.Figure([go.Pie(labels=m,values=v)])
    return render_template("sobre.html",grafico=pie.to_html())

#Remover gasto
@app.route('/remove/<id>',methods=['GET','POST'])
def remove(id):
    g = Gasto.query.get(id)
    db.session.delete(g)
    db.session.commit()
    return redirect(url_for('gastos'))

#Login
@app.route('/perfil/<id>')
@login_required
def perfil(id):
    if int(id)==int(current_user.id):
        return render_template('perfil.html',id=id)

#Sair
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

#Add gasto
@app.route('/addgasto',methods=['GET','POST'])
@login_required
def addgasto():
    form = FormAddGasto()
    gastos = Gasto.query.filter_by(id_usuario=int(current_user.id)).all()
    form.categoria.choices = gastos_manager.get_categorias(gastos)

    if form.validate_on_submit() and current_user and len(current_user.conta)>0:
        gasto = Gasto()
        gasto.descricao=form.descricao.data
        gasto.valor=form.valor.data
        if form.input_categoria.data.strip()=="":
            gasto.categoria=form.categoria.data
        else:
            gasto.categoria=form.input_categoria.data
        gasto.id_usuario=int(current_user.id)
        db.session.add(gasto)
        db.session.commit()

        conta = current_user.conta[0]
        conta.saldo-=gasto.valor
        db.session.add(conta)
        db.session.commit()

        return redirect(url_for('gastos'))
    return render_template('add_gasto.html',form=form)

#Gastos
@app.route("/gastos", methods=['GET','POST'])
@login_required
def gastos():
    
    form = Periodo()
    form.di.choices=['Todos','Hoje','Semana','Mês']
    if form.validate_on_submit:
        print(form.di.data)
    lista_gastos = Gasto.query.filter_by(id_usuario=current_user.id).all()
    gc = gastos_manager.get_gastos_categoria(lista_gastos)
    gm = gastos_manager.get_gastos_mes(lista_gastos)

    gd = gastos_manager.valor_gastos_dia(lista_gastos)
    gs = gastos_manager.valor_gastos_semana(lista_gastos)
    gmes = gastos_manager.valor_gastos_mes(lista_gastos)
    gt = gastos_manager.valor_todos_gastos(lista_gastos)

    vg = {'gd':gd,'gs':gs,'gm':gmes,'gt':gt}
    
    lc =[]
    lv = []
    meses = []
    valor = []
    for i in gc:
        lc.append(i['categoria'])
        lv.append(i['valor'])
    for i in gm:
        meses.append(i['mes'])
        valor.append(i['valor'])
    #fgm = go.Figure([go.Bar(x=meses,y=valor)])
    #fgm.update_layout(plot_bgcolor="#b0a8b3",paper_bgcolor='#b0a8b3')
    gt = gastos_manager.gastos_por_periodo(lista_gastos,'20/06/2025','10/08/2025')
    print(gt)

    return render_template("gastos.html",lista_gastos=lista_gastos,lc=lc,lv=lv,meses=meses,valor=valor,form=form,vg=vg)

@app.route("/receitas", methods=['GET','POST'])
@login_required
def receitas():
    receitas = Receita.query.filter_by(id_usuario=int(current_user.id)).all()
    rm  = receitas_manager.ReceitaManager(receitas)
    vd = rm.valor_hoje()
    vs = rm.valor_semana()
    vm = rm.valor_mes()
    vt = rm.valor_total()
    vr = {'vd':vd,'vs':vs,'vm':vm,'vt':vt}
    return render_template("receitas.html",receitas=receitas,vr=vr)

#Add Receita
@app.route("/addreceita",methods=['GET','POST'])
@login_required
def addreceita():
    form = AddReceita()
    if form.validate_on_submit():
        receita = Receita()
        receita.fonte=form.fonte.data
        receita.valor=float(form.valor.data)
        receita.data=form.rdata.data
        receita.id_usuario=int(current_user.id)
        db.session.add(receita)
        db.session.commit()
        if len(current_user.conta)>0:
            conta = current_user.conta[0]
            conta.saldo+=float(form.valor.data)
            db.session.add(conta)
            db.session.commit()

        return redirect(url_for("receitas"))
    return render_template("add_receita.html",form=form)
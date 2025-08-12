from datetime import datetime
import calendar
from site_flask import util

def get_categorias(lista:list):
        categorias = []
        for g in lista:
            if str(g.categoria).strip() not in categorias:
                categorias.append(str(g.categoria))
        return categorias

def get_valor_total(lista:list):
    valor = 0.0
    for g in lista:
          valor+=float(g.valor)
    return valor

def get_gastos_categoria(lista:list):
    categorias = get_categorias(lista)
    gastos_categoria = []
    for ct in categorias:
        dc = {'categoria':ct,'valor':0,'porcentagem':0}
        for g in lista:
            if str(ct)==str(g.categoria):
                dc['valor']+=g.valor
        dc['porcentagem']=float(round(dc['valor']*100/get_valor_total(lista),2))
        gastos_categoria.append(dc)

    return gastos_categoria

def get_gastos_mes(lista:list):
        meses = ['Jan','Fev','Mar','Abr','Mai','Jun','Jul','Ago','Set','Out','Nov','Dez']
        l = []
        mes_atual = int(datetime.today().strftime('%m'))
        y = int(datetime.today().strftime('%Y'))
        
        for i in range(0,mes_atual):
            valor = 0.0
            di = datetime.strptime("01/{}/{}".format(i+1,y),"%d/%m/%Y")
            df = datetime.strptime("{}/{}/{}".format((calendar.monthrange(y,i+1)[1]),i+1,y),"%d/%m/%Y")
            for g in lista:
                    gd = datetime.strptime(g.data,"%d/%m/%Y")
                    if gd>=di and gd<=df:
                        valor = valor+g.valor
            l.append({'mes':meses[i],'valor':valor})
        
        return l

def gastos_por_periodo(lista:list,di,df):
    l = []
    di = datetime.strptime(di,'%d/%m/%Y')
    df = datetime.strptime(df,'%d/%m/%Y')
    for g in lista:
         data = datetime.strptime(g.data,'%d/%m/%Y')
         if data>=di and data<=df:
            l.append(g)
    return l

def valor_gastos_periodo(lista:list,di,df):
    l = gastos_por_periodo(lista,di,df)
    valor = 0.0
    for g in l:
        valor+=g.valor
    return valor


def valor_gastos_dia(lista:list):
    return valor_gastos_periodo(lista,util.today(),util.today())

def valor_gastos_semana(lista:list):
     return valor_gastos_periodo(lista,util.first_day_week(),util.today())

def valor_gastos_mes(lista:list):
     return valor_gastos_periodo(lista,util.first_day_mes(),util.today())

def valor_todos_gastos(lista:list):
     return round(valor_gastos_periodo(lista,'01/01/2025',util.today()),2)
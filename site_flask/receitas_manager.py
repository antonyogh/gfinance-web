from datetime import datetime
import calendar
from site_flask import util

class ReceitaManager():
      def __init__(self,lista:list):
            self.lista=lista
            
      def get_receita_periodo(self,di,df):
        l = []
        di = datetime.strptime(di,'%d/%m/%Y')
        df = datetime.strptime(df,'%d/%m/%Y')

        for g in self.lista:
            dg = datetime.strptime(g.get_data(),'%d/%m/%Y')
            if(dg>=di and dg<=df):
                l.append(g)
        return l
      
      def get_gastos_mes(self):
        meses = ['Jan','Fev','Mar','Abr','Mai','Jun','Jul','Ago','Set','Out','Nov','Dez']
        l = []
        mes_atual = int(datetime.today().strftime('%m'))
        y = int(datetime.today().strftime('%Y'))
        
        for i in range(0,mes_atual):
            valor = 0.0
            di = "01/{}/{}".format(i+1,y)
            df = "{}/{}/{}".format((calendar.monthrange(y,i+1)[1]),i+1,y)
            for r in self.lista:
                    if r.data>=di and r.data<=df:
                        valor = valor+r.valor
            l.append({'mes':meses[i],'valor':valor})
        
        return l
      
      def valor_periodo(self,di,df):
          l = []
          di = datetime.strptime(di,'%d/%m/%Y')
          df = datetime.strptime(df,'%d/%m/%Y')
          valor =0.0
          for r in self.lista:
              data = datetime.strptime(r.data,'%d/%m/%Y')
              if data>=di and data<=df:
                 valor+=r.valor
          return valor

      
      def valor_hoje(self):
          return self.valor_periodo(util.today(),util.today())
      
      def valor_semana(self):
          return self.valor_periodo(util.first_day_week(),util.today())
      
      def valor_mes(self):
          return round(self.valor_periodo(util.first_day_mes(),util.today()),2)
      
      def valor_total(self):
          return round(float(self.valor_periodo('01/01/2025',util.today())),2)
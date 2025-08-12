from datetime import datetime
import calendar

def today():
    return datetime.strftime(datetime.today(),'%d/%m/%Y')

def first_day_week():
    d = datetime.today().day
    m = datetime.today().month
    y = datetime.today().year
    calendar.setfirstweekday(calendar.SUNDAY)
    c = calendar.monthcalendar(y,m)
    pds = 0
    for w in c:
        if d in w:
            pds = w[0]
    return "{}/{}/{}".format(pds,m,y)

def first_day_mes():
     mes = datetime.strftime(datetime.now(),'%m')
     ano = datetime.strftime(datetime.now(),'%Y')
     di = str('01/{}/{}'.format(mes,ano))
     return di

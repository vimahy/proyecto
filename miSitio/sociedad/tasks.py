from celery.task.schedules import crontab
from celery.decorators import periodic_task
import django
from datetime import datetime, timedelta


from account.models import*
from django.contrib.auth.models import User
from account.models import*
from account.models import*
from django.template.loader import render_to_string, get_template
from django.core.mail import EmailMessage
from django.core.mail import send_mail



import time



hoy = datetime.date.today()

#Solo tomamos en cuenta a los socios con cuotas vigentes
todos= Account.objects.filter(cuota__fecha_fin__gte=hoy).distinct()



@periodic_task(run_every=(crontab(minute='*/1')), name="suma", ignore_result=True)
def prueba_suma(x, y):
    return x + y
    

@periodic_task(run_every=(crontab(minute='*/1')), name="hola", ignore_result=True)
def some_task():
    print("HOLLAAA")
    # do something

@periodic_task(run_every=crontab(minute=0, hour=0), name="prueba", ignore_result=True)
def every_monday_morning():
    print("Execute every day at 7:30AM.")

#Funcion que envia correos de recordatotio

@periodic_task(run_every=crontab(minute=0, hour=7), name="recordatorio", ignore_result=True)
def recordatorio_cuota():
    for a in todos:
        cuota = a.cuota_set.last()
        ultima = cuota.fecha_fin
        fecha_limite = hoy + timedelta(days=1)
        fecha_anticipada = hoy + timedelta(days=15)
        if fecha_limite > ultima:
            print("Mndar mensaje 15 dias faltantes")
            print(ultima)
        elif fecha_limite > ultima:
            print("Mandar mensaje final")
            print(ultima)
        else:
            print("Aun no vence")
            print (ultima)

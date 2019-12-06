import django
import time

from celery.task.schedules import crontab
from celery.decorators import periodic_task
from datetime import datetime, timedelta
from account.models import*
from django.contrib.auth.models import User
from account.models import*
from django.template.loader import render_to_string, get_template
from django.core.mail import EmailMessage
from django.core.mail import send_mail



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


#Solo tomamos en cuenta a los socios con cuotas vigentes
todos= Account.objects.filter(cuota__fecha_fin__gte=hoy).distinct()
@periodic_task(run_every=crontab(minute=0, hour=7), name="recordatorio", ignore_result=True)
def recordatorio_cuota():
    hoy = datetime.date.today()
    todos= Account.objects.filter(cuota__fecha_fin__gte=hoy).distinct()
    subject = "Su membrecia esta a punto de vencer"
    from_email = 'smf.soporte@ciencias.unam.mx'
    primer_recordatorio = '/home/victor/proyecto/miSitio/miSitio/templates/base.html'
    segundo_recordatorio = '/home/victor/proyecto/miSitio/miSitio/templates/base.html'
    for socio in todos:
        ctx = {
        "username": socio.user.first_name,
        "last_name": socio.user.last_name
        }
        # Hay socios sin correo
        if socio.user.email == ' ' or socio.user.email == '  ':
            pass
        else:
            cuota = socio.cuota_set.last()
            ultima = cuota.fecha_fin
            to = to =[socio.user.email]
            if ultima -hoy == datetime.timedelta(15):
                print("Mndar mensaje 15 dias faltantes")
                message = render_to_string(primer_recordatorio, ctx)
                msg = EmailMessage(subject, message,to=to, from_email= from_email)
                msg.send()
            elif ultima -hoy ==datetime.timedelta(1):
                print("Mandar mensaje final")
                print(ultima)
                message = render_to_string(segundo_recordatorio, ctx)
                msg = EmailMessage(subject, message,to=to,from_email=from_email)
                msg.send()
            else:
                pass

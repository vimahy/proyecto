# encoding=utf8
import datetime
from django.core.exceptions import ObjectDoesNotExist
from django import template
from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.contrib.postgres.search import SearchVector
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.http import HttpResponse
from account.models import *
from django.http import HttpResponseRedirect
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
import sys  



def xstr(s):
    if s is None:
        return ' '
    return str(s)




#def creaTarjetas(socios,request):
def creaTarjetas(socios):
     """Imprime la informacion de los socios.
     """
     socios2 = socios.order_by('domicilioprofesional__codigo_postal')
     #Ordenar a los socios con respecto a los codigos postales de sus direcciones
     # Create the HttpResponse object with the appropriate PDF headers.
     response = HttpResponse(content_type='application/pdf')
     response['Content-Disposition'] = 'attachment; filename="somefilename.pdf"'
     p = canvas.Canvas(response)
     # Create the HttpResponse object with the appropriate PDF headers.
     #response = HttpResponse(content_type='application/pdf')
     #response['Content-Disposition'] = 'attachment; filename="tarjetas.pdf"'
     # Create the PDF object, using the response object as its "file."
 #Un punto es igual a 0.035285715 cm
     p = canvas.Canvas('tarjetas.pdf',pagesize=	A4)
     #p = canvas.Canvas(response)
     ancho = 198.380562786
     largo = largo = 510.121447164
     # Si se recibe una colleccion
     if hasattr(socios2, '__iter__'):
         for socio in socios2:
             #p.rect(ancho, largo, 340.080964776, 90.688257274)
             #if socio.domicilioprofesional:
             try:
                 if socio.domicilioprofesional:
                     t = xstr(socio.calidad)+"/"+ xstr(socio.numero_socio)+"/"+xstr(socio.cuota_set.last())
                     u = xstr(socio.user.first_name)+" "+xstr(socio.user.last_name)+" "+xstr(socio.apellido_materno)
                     v = socio.domicilioprofesional.institucion
                     w = socio.domicilioprofesional.dependencia
                     x = socio.domicilioprofesional.calle_numero_apartado_postal
                     y = socio.domicilioprofesional.colonia
                     z = "C.P."+ "%05d" % socio.domicilioprofesional.codigo_postal+' '+xstr(socio.domicilioprofesional.municipio_ciudad)+' '+xstr(socio.domicilioprofesional.estado)
                     print(socio.domicilioprofesional.codigo_postal)
                     print(socio.numero_socio)
                 if socio.domicilio:
                     t = xstr(socio.calidad)+"/"+ xstr(socio.numero_socio)+"/"+xstr(socio.cuota_set.last())
                     u = xstr(socio.grado_academico)+" "+xstr(socio.user.first_name)+" "+xstr(socio.user.last_name)+" "+xstr(socio.apellido_materno)
                     v = socio.domicilio.calle_numero_apartado_postal
                     w = socio.domicilio.colonia
                     x = socio.domicilio.municipio_delegacion
                     y = xstr(socio.domicilio.ciudad)+" "+xstr(socio.domicilio.estado)
                     z = ""
             except (ObjectDoesNotExist):
                 t = " "
                 u = " "
                 v = " "
                 w = " "
                 x = " "
                 y = " "
                 z = " "
             p.drawString(ancho+5,largo+90,t)
             p.drawString(ancho+5,largo+75,u)
             p.drawString(ancho+5,largo+60,v)
             p.drawString(ancho+5,largo+45,w)
             p.drawString(ancho+5,largo+30,x)
             p.drawString(ancho+5,largo+15,y)
             p.drawString(ancho+5,largo ,z)
             p.showPage()
     else:
         #p.rect(ancho, largo, 340.080964776, 90.688257274)
         t = xstr(socios.calidad)+"/"+ xstr(socios.numero_socio)+"/"+xstr(socios.cuota_set.last())
         u = xstr(socios.grado_academico)+" "+xstr(socios.user.first_name)+" "+xstr(socios.user.last_name)+" "+xstr(socios.apellido_materno)+" "+p.drawString(ancho+5,largo+30,x)
         p.drawString(ancho+5,largo+15,y)
         p.drawString(ancho+5,largo ,z)
         p.showPage()
     p.save()
     return response



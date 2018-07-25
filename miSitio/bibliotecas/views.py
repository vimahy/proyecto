# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from bibliotecas.models import*
from django.shortcuts import render

# Create your views here.
# encoding=utf8
import datetime
from django.core.exceptions import ObjectDoesNotExist
from django import template
from django.core.urlresolvers import reverse
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


reload(sys)  
sys.setdefaultencoding('utf8')
register = template.Library()




#def creaTarjetas(socios,request):
def creaTarjetas(bibliotecas):
     """Imprime la informacion de los socios.
     """
     bibliotecas2 = bibliotecas.order_by('codigo_postal')
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
     p = canvas.Canvas('bibliotecas.pdf',pagesize=letter)
     #p = canvas.Canvas(response)
     ancho = 198.380562786
     largo = 510.121447164
     # Si se recibe una colleccion
     for biblioteca in bibliotecas2:
         try:
             if biblioteca.codigo:
                 t = xstr(biblioteca.nombre)
                 u = xstr(biblioteca.institucion)
                 v = xstr(biblioteca.calle_numero)
                 w = xstr(biblioteca.ciudad_y_estado)
                 x = xstr(biblioteca.apartado_postal)
                 y = xstr(biblioteca.colonia)
                 z = "C.P."+ "%05d" % biblioteca.codigo_postal
                 print(biblioteca.codigo_postal)
                 print(biblioteca.nombre)
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
     # cerrar el objeto PDF
     p.save()
     return response

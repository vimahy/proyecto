from django.conf.urls import url
from django.contrib.auth.forms import UserCreationForm

from . import views

urlpatterns = [
    url(r'^tarjetas$', views.tarjetas, name='tarjetas'),
    url(r'^cargar/socio$', views.cargar_socio, name='cargar_socio'),
    url(r'^socio/(?P<pk>[0-9]+)/$', views.detalle_socio),
    url(r'^editar/(?P<pk>[0-9]+)/socio/$', views.editar_socio, name='editar_socio'),
    url(r'^cargar/cuota/$', views.cargar_cuota, name='cargar_cuota'),
    url(r'^agregar/(?P<pk>[0-9]+)/cuota/$', views.agregar_cuota, name='agregar_cuota'),
    url(r'^cuota/(?P<pk>[0-9]+)/$', views.detalle_cuota),
    url(r'^editar/(?P<pk>[0-9]+)/$', views.editar_cuota, name='editar_cuota'),
    url(r'^cargar/publicacion$', views.cargar_publicacion, name='cargar_publicacion'),
    url(r'^publicacion/(?P<pk>[0-9]+)/$', views.detalle_publicacion),
    url(r'^editar/(?P<pk>[0-9]+)/publicacion/$', views.editar_publicacion, name='editar_publicacion'),
    url(r'^cargar/domicilio/$', views.cargar_domicilio, name='cargar_domicilio'),
    url(r'^domicilio/(?P<pk>[\w\s\D]+)/$', views.detalle_domicilio),
    url(r'^editar/(?P<pk>[\w\s\D]+)/domicilio$', views.editar_domicilio, name='editar_domicilio'),
    url(r'^socio/(?P<pk>[0-9]+)/cuotas/$', views.lista_cuotas),
    url(r"^prueba/$", views.signup, name="prueba"),
]

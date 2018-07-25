# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

class Biblioteca(models.Model):
    codigo = models.CharField(max_length=200,null=True)
    nombre = models.CharField(max_length=200,null=True)
    institucion = models.CharField(max_length=200, null=True)
    codigo_postal = models.PositiveIntegerField(
                                        default=0,
                                        blank=True,
                                        null=True,)
    calle_numero = models.CharField(max_length=200, null =True)
    apartado_postal = models.CharField(max_length=200,null=True)
    colonia = models.CharField(max_length=200,
                                        blank=True,
                                        null=True,)
    ciudad_y_estado = models.CharField(max_length=200,null=True)
    def __str__(self):
        return self.codigo or u''

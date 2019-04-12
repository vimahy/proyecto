from .serializers import  UserSerializer
from django.contrib.auth.models import User
from .models import Account, Cuota
import datetime

from rest_framework import generics




class AccountList(generics.ListCreateAPIView):
    # Los pagos deben ser desde el primer dia del agno en curso
    # hasta el momento. Considerar tambien a los socios vitalicios.
    # Sus cuotas tienen una duracion de 20 agnos 
    cuota= Account.objects.filter(cuota__fecha_pago__gte='2019-1-1').distinct()
    queryset = User.objects.filter(id__in=cuota).distinct()
    #queryset = User.objects.all()
    serializer_class = UserSerializer



class AccountDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()

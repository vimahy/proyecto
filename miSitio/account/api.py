from .serializers import  UserSerializer
from django.contrib.auth.models import User
from .models import Account

from rest_framework import generics


class AccountList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer



class AccountDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()

from account.models import*
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated



class UserSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(read_only=True)
    last_name = serializers.CharField(read_only=True)
    email = serializers.CharField(read_only=True)
    apellido_materno = serializers.CharField(source="account.apellido_materno",read_only=True)
    vencimiento= serializers.CharField(source="account.cuota_set.last",read_only=True)
    class Meta:	
        model = User
        fields = ('first_name', 'last_name','apellido_materno','email','vencimiento')








from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User

class  ProfileSerailizer(serializers.Serializer):
    class Meta:
        model=Profile
        fields=('firstname','lastname','user','email','mobile')


class UserSerializer(serializers.Serializer):
    class Meta:
        model=User
        fields=('url','username','email','groups')



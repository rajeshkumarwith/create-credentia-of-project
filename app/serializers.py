from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User

class  ProfileSerailizer(serializers.Serializer):
    class Meta:
        model=Profile
        fields=('firstname','lastname','user','email','mobile')

class ProfileDataSerializer(serializers.Serializer):
    keys=serializers.CharField(max_length=1000)
    ctr=serializers.IntegerField()
    impressions=serializers.IntegerField()
    position=serializers.IntegerField()
    clicks=serializers.IntegerField()

class UserSerializer(serializers.Serializer):
    class Meta:
        model=User
        fields=('url','username','email','groups')


# class ProfiledataSerializer(serializers.Serializer):
#     id=serializers.IntegerField()
from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User

class  ProfileSerailizer(serializers.Serializer):
    class Meta:
        model=Profile
        fields=('firstname','lastname','email','username','mobile','start_time','end_time')

class ProfileDataSerializer(serializers.Serializer):
    query=serializers.CharField(max_length=1000)
    # country=serializers.CharField(max_length=100)
    # device=serializers.CharField(max_length=100)
    # page=serializers.CharField(max_length=500)
    ctr=serializers.IntegerField()
    impressions=serializers.IntegerField()
    position=serializers.IntegerField()
    clicks=serializers.IntegerField()


class  ProfiledataSerializer(serializers.Serializer):
    query=serializers.CharField(max_length=100)
    page=serializers.CharField(max_length=100)
    country=serializers.CharField(max_length=100)
    device=serializers.CharField(max_length=100)
    ctr=serializers.IntegerField()
    position=serializers.IntegerField()
    

class PageDataSerializer(serializers.Serializer):
    page=serializers.CharField(max_length=500)
    ctr=serializers.IntegerField()
    impressions=serializers.IntegerField()
    position=serializers.IntegerField()
    clicks=serializers.IntegerField()
    
class UserSerializer(serializers.Serializer):
    class Meta:
        model=User
        fields=('url','username','email','groups')



from rest_framework import serializers
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['username', 'email', 'first_name', 'last_name','mobile']

from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User

class  ProfileSerailizer(serializers.Serializer):
    class Meta:
        model=Profile
        fields=('firstname','lastname','email','username','mobile','start_time','end_time')

class ProfileDataSerializer(serializers.Serializer):
    query=serializers.CharField(max_length=1000)
    country=serializers.CharField(max_length=100)
    device=serializers.CharField(max_length=100)
    page=serializers.CharField(max_length=500)
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
    
class QueryRelatedSerializer(serializers.Serializer):
    query=serializers.CharField(max_length=100)
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



# from rest_framework import serializers
# from django.contrib.auth.models import User

# class UserdSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Profile
#         fields = ['username', 'email', 'first_name', 'last_name','mobile']






class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id','first_name','last_name','email','phone_no')


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','email','username','password')
        extra_kwargs = {
            'password':{'write_only': True},
        }
    def create(self, validated_data):
        user = User.objects.create_user(validated_data['email'],
                                        password = validated_data['password'],
                                        username = validated_data['username'],
                                        
                                    )

        return user



class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=200)
    password = serializers.CharField(max_length=200)




class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model=Project
        fields=('user','name','slug')



class CheckListSerializer(serializers.ModelSerializer):
    class Meta:
        model=CheckList
        fields=('name','project','IsCompleted')



class ResetPasswordSerializer(serializers.ModelSerializer):
    def validate(self,attrs):
        email=attrs.get('email')
        password=attrs.get('password')
        data=User.objects.filter(email=email,password=password)
        if data:
            return serializers.ValidationError('already exists')
        # return super().validate(attrs)
    class Meta:
        fields=('email','password')



class SearchConsoleResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = SearchConsoleResponse
        fields = '__all__'
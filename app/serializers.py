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






# class UserSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = User
#         fields = ('id','first_name','last_name','email','phone_no')

from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'google_id', 'picture', 'first_name', 'last_name')



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




# class ProjectSerializer(serializers.ModelSerializer):
#     class Meta:
#         model=Project
#         fields=('user','name','slug')



# class CheckListSerializer(serializers.ModelSerializer):
#     class Meta:
#         model=CheckList
#         fields=('name','project','IsCompleted')



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


class SearchSerailizer(serializers.ModelSerializer):
    # keyword = serializers.ListField()
    # keyword = serializers.ListField(child=serializers.CharField())

    class Meta:
        model=SearchConsoleData
        fields=('id','project','keyword','clicks','ctr','impressions','position')


class SearchDataSerializer(serializers.ModelSerializer):
    class Meta:
        model=SearchConsoleData
        fields=('keyword',)

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model=Question
        fields=('question_text','pub_date','author','category')

# serializers.py

# from rest_framework import serializers
# from .models import Book

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

import sys
from django.conf import settings
# from modules.library.sociallib import google
from rest_framework import serializers
from django.conf import settings
from library.sociallib import google
from library.register.register import register_social_user

from rest_framework.exceptions import AuthenticationFailed

class GoogleSocialAuthSerializer(serializers.Serializer):
    auth_token = serializers.CharField()

    def validate_auth_token(self, auth_token):
        user_data = google.Google.validate(auth_token)
        try:
            user_data['sub']
        except:
            raise serializers.ValidationError(
                'The token is invalid or expired. Please login again.'
            )
        print(user_data['aud'])
        if user_data['aud'] != '286943146870-h21okc0jtogcva4mrmi28h4fpkcaagum.apps.googleusercontent.com':

            raise AuthenticationFailed('oops, who are you?')

        user_id = user_data['sub']
        email = user_data['email']
        name = user_data['name']
        provider = 'google'

        return register_social_user(
            provider=provider, user_id=user_id, email=email, name=name)


class SearchConsoleDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = SearchConsoleData
        fields = '__all__'




class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model=Project
        fields='__all__'

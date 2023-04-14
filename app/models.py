from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Profile(models.Model):
    firstname=models.CharField(max_length=100,blank=True,null=True)
    lastname=models.CharField(max_length=100,blank=True,null=True)
    username=models.CharField(max_length=100,blank=True,null=True)
    email=models.EmailField()
    mobile=models.CharField(max_length=20,blank=True,null=True)
    start_time=models.TimeField()
    end_time=models.TimeField()


    

class Friend(models.Model):
    User_id=models.ForeignKey(User,on_delete=models.CASCADE)
    OtherUser_id=models.ForeignKey(User,on_delete=models.CASCADE,related_name='otheruser')
    DateAdded=models.DateTimeField(blank=True,null=True)


from django.db import models
from allauth.socialaccount.models import SocialApp

class SearchConsoleCredential(models.Model):
    social_app = models.ForeignKey(SocialApp, on_delete=models.CASCADE)
    access_token = models.CharField(max_length=200)
    refresh_token = models.CharField(max_length=200)
    token_uri = models.CharField(max_length=200)
    expires_at = models.DateTimeField()



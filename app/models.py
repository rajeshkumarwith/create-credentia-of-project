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




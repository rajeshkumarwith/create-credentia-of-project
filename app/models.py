from django.db import models

# Create your models here.
class Profile(models.Model):
    firstname=models.CharField(max_length=100,blank=True,null=True)
    lastname=models.CharField(max_length=100,blank=True,null=True)
    username=models.CharField(max_length=100,blank=True,null=True)
    email=models.EmailField()
    mobile=models.CharField(max_length=20,blank=True,null=True)


    
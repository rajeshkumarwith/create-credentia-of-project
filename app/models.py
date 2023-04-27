from django.db import models
# from django.contrib.auth.models import User
# Create your models here.
class Profile(models.Model):
    firstname=models.CharField(max_length=100,blank=True,null=True)
    lastname=models.CharField(max_length=100,blank=True,null=True)
    username=models.CharField(max_length=100,blank=True,null=True)
    email=models.EmailField()
    mobile=models.CharField(max_length=20,blank=True,null=True)
    start_time=models.TimeField()
    end_time=models.TimeField()


    

# class Friend(models.Model):
#     User_id=models.ForeignKey(User,on_delete=models.CASCADE)
#     OtherUser_id=models.ForeignKey(User,on_delete=models.CASCADE,related_name='otheruser')
#     DateAdded=models.DateTimeField(blank=True,null=True)


from django.db import models

# class SearchConsoleCredential(models.Model):
#     social_app = models.ForeignKey(SocialApp, on_delete=models.CASCADE)
#     access_token = models.CharField(max_length=50)
#     refresh_token = models.CharField(max_length=50)
#     token_uri = models.CharField(max_length=50)
#     expires_at = models.DateTimeField()



from django.db import models
from django.contrib.auth.base_user import BaseUserManager
# from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AbstractUser
# from django.contrib.auth.models import User

from django.conf import settings

from django.conf import settings
User = settings.AUTH_USER_MODEL
# Create your models here.



class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The Email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(email, password, **extra_fields)


class CustomUserManager(BaseUserManager):
  
    def create_user(self, email, password, **extra_fields):
   
        if not email:
            raise ValueError('The Email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(email, password, **extra_fields)



class User(AbstractUser):
    username=models.CharField(max_length=100)
    email = models.EmailField('email address', unique=True)
    phone_no=models.CharField(max_length=100)
    first_name=models.CharField(max_length=100)
    last_name=models.CharField(max_length=100)
    # password=models.CharField(max_length=200)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    spouse_name = models.CharField(blank=True, max_length=100)
    date_of_birth = models.DateField(blank=True, null=True)
    

    def __str__(self):
        return self.email
    





class Project(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    name=models.CharField(max_length=100)
    slug=models.SlugField(max_length=100)

    def __str__(self):
        return self.name
    
    # def get_absolute_url(self):
    #     return reverse("article_detail", kwargs={"slug": self.slug})
    
    
class CheckList(models.Model):
    name=models.CharField(max_length=100)
    project=models.ForeignKey(Project,on_delete=models.CASCADE)
    is_completed=models.BooleanField(default=False)

    def __str__(self):
        return self.name
    


from django.db import models

class SearchConsoleResponse(models.Model):
    site_url = models.CharField(max_length=255)
    keyword = models.CharField(max_length=255)
    response = models.JSONField()




class SearchAnalytics(models.Model):
    date = models.DateField()
    clicks = models.IntegerField()
    impressions = models.IntegerField()
    ctr = models.FloatField()
    position = models.FloatField()

    
class SearchConsoleData(models.Model):
    query = models.CharField(max_length=255)
    clicks = models.IntegerField()
    ctr = models.FloatField()
    impressions = models.IntegerField()
    position = models.FloatField()
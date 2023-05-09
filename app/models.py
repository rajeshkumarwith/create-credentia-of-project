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


    

    
# from django.contrib.auth.models import AbstractUser


# class User(AbstractUser):
#     email = models.EmailField(unique=True)
#     google_id = models.CharField(max_length=255, null=True, blank=True)
#     picture = models.URLField(null=True, blank=True)
#     first_name = models.CharField(max_length=255, null=True, blank=True)
#     last_name = models.CharField(max_length=255, null=True, blank=True)

#     def __str__(self):
#         return self.username




# class Project(models.Model):
#     user=models.ForeignKey(User,on_delete=models.CASCADE)
#     name=models.CharField(max_length=100)
#     slug=models.SlugField(max_length=100)

#     def __str__(self):
#         return self.name
    
#     # def get_absolute_url(self):
    #     return reverse("article_detail", kwargs={"slug": self.slug})
    
    
# class CheckList(models.Model):
#     name=models.CharField(max_length=100)
#     project=models.ForeignKey(Project,on_delete=models.CASCADE)
#     is_completed=models.BooleanField(default=False)

#     def __str__(self):
#         return self.name
    


from django.db import models




class Search(models.Model):
    project=models.CharField(max_length=100)
    keyword=models.CharField(max_length=150)
    clicks=models.IntegerField()
    ctr=models.IntegerField()
    impressions=models.IntegerField()
    position=models.IntegerField()

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published', null=True)
    author = models.CharField(max_length=200, null=True)
    category=models.CharField(max_length=100)
    def __str__(self):
        return self.author



class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    genre = models.CharField(max_length=100)



# class User(models.Model):
#     name = models.CharField(max_length=100)

from django.contrib.auth import get_user_model
User = get_user_model()

class Project(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return str(self.name)

class SearchResult(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    keyword = models.CharField(max_length=100)
    clicks = models.IntegerField()
    ctr = models.FloatField()
    impressions = models.IntegerField()
    position = models.FloatField()
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.project
    





class SearchConsoleData(models.Model):
    project = models.CharField(max_length=255,blank=True,null=True)
    keyword = models.CharField(max_length=255)
    clicks = models.IntegerField()
    ctr = models.FloatField()
    impressions = models.IntegerField()
    position = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)


    def save(self, *args, **kwargs):
        self.position = round(self.position, 2)
        super(SearchConsoleData, self).save(*args, **kwargs)

class DomainVerification(models.Model):
    domain_name = models.CharField(max_length=255)
    verification_code = models.CharField(max_length=255, null=True, blank=True)
    verified = models.BooleanField(default=False)


class Domain(models.Model):
    name = models.CharField(max_length=255)


class GoogleSearchConsoleToken(models.Model):
    email = models.EmailField()
    password = models.CharField(max_length=255)
    access_token = models.CharField(max_length=255)



class GoogleToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    access_token = models.CharField(max_length=255)
    refresh_token = models.CharField(max_length=255)
    expires_at = models.DateTimeField()


class GoogleSearchConsoleTokenData(models.Model):
    token = models.CharField(max_length=255)
    refresh_token = models.CharField(max_length=255)



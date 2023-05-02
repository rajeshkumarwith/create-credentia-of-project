from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
# Create your models here.
# from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _


from django.contrib.auth.base_user import BaseUserManager,AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin


class UserAccountManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
 
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.base_user import BaseUserManager
from django.utils import timezone


class UserManager(BaseUserManager):
    def create_user(
        self, email, password=None, is_staff=False, is_active=True, is_superuser=False, **extra_fields
    ):
        """Create a user instance with the given email and password."""
        email = UserManager.normalize_email(email)
        extra_fields.pop("username", None)
        user = self.model(
            email=email, is_active=is_active, is_staff=is_staff, is_superuser=is_superuser ,**extra_fields
        )
        if password:
            user.set_password(password)
        user.save()
        return user
    def create_superuser(self, email, password=None, **extra_fields):
        return self.create_user(
            email, password, is_staff=True, is_superuser=True, **extra_fields
        )
    # def users(self):
    #     return self.get_queryset().filter(
    #         Q(is_staff=False) & Q(is_superuser=False)
    #     )
class User(PermissionsMixin, AbstractBaseUser):
    email = models.EmailField(unique=True)
    username=models.CharField(max_length=100)
    first_name = models.CharField(max_length=256, blank=True)
    last_name = models.CharField(max_length=256, blank=True)
    phone_no = models.CharField(max_length=15, blank=True)
    password = models.CharField(max_length=15, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)


    USERNAME_FIELD = "email"

    objects = UserManager()

    class Meta:
        ordering = ("email",)

    def __str__(self):
        return self.email



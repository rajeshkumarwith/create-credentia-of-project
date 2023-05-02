from django.contrib import admin
from django.urls import path,include
from doddle import views
from .views import *


urlpatterns = [
    path('signup/',RegisterUserAPIView.as_view(),name='signup'),
    path('login/',LoginApi.as_view(),name='login')

]






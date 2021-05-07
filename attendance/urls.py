from django.urls import include, path
from .views import *

urlpatterns = [
    path('',index, name='index'),
    path('login',UserLogin, name='login'),
    path('register',Register, name='register'),
]
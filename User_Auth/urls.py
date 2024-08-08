from django.urls import path

from .views import signup_api

urlpatterns = [
    path('signup/',signup_api,name='signup'),
    ]
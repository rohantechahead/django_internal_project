from django.urls import path
from . views import login,signup_api

urlpatterns= [
    path('signup/',signup_api,name='signup'),
    path('login/', login, name='login'),
]

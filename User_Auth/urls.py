from django.urls import path
from . views import user_login,signup_api,update_profile

urlpatterns= [
    path('signup/',signup_api,name='signup'),
    path('login/', user_login, name='login'),
    path('update_profile/',update_profile,name='update-profile')
]

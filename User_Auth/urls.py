from django.urls import path
from . views import user_login,signup_api, user_logout

urlpatterns = [
    path('signup/',signup_api,name='signup'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
]

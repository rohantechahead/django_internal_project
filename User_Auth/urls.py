from django.urls import path
from .views import user_login, signup_api, update_profile, user_logout, get_profile,user_delete
urlpatterns = [
    path('signup/', signup_api, name='signup'),
    path('login/', user_login, name='login'),
    path('update_profile/', update_profile, name='update-profile'),
    path('logout/', user_logout, name='logout'),
    path('profile/',get_profile,name='profile'),
    path('delete/',user_delete, name='delete'),
]

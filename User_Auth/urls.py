from django.urls import path
from .views import user_login, signup_api, forgot_password_api, update_security_q_a, delete_security_q_a, \
    get_security_q_a
from .views import user_login, signup_api, update_profile, user_logout



urlpatterns = [
    path('signup/', signup_api, name='signup'),
    path('login/', user_login, name='login'),
    path('forgot_password/',forgot_password_api,name='forgot_password'),
    path('update/',update_security_q_a,name='update'),
    path('delete/',delete_security_q_a,name='delete'),
    path('getquestion/',get_security_q_a,name='getquestion'),

    path('update_profile/', update_profile, name='update-profile'),
    path('logout/', user_logout, name='logout'),


]


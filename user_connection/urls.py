from django.urls import path

from user_connection.views import send_request, block_user

urlpatterns = [
    path('send-request/', send_request, name='send-request'),
    path('block-user/', block_user, name='block-user'),

]

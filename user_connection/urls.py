from django.urls import path

from user_connection.views import send_request, block_user, withdraw_send_request

urlpatterns = [
    path('send-request/', send_request, name='send-request'),
    path('block-user/', block_user, name='block-user'),
    path('withdraw-request/', withdraw_send_request, name='withdraw-request')
]

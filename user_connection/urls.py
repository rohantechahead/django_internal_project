from django.urls import path
<<<<<<< Updated upstream

from user_connection.views import handle_friend_request,send_request, block_user, withdraw_send_request
=======
from user_connection.views import handle_friend_request,send_request,withdraw_send_request
>>>>>>> Stashed changes

urlpatterns = [

    path('accept-reject/', handle_friend_request, name='accept-reject'),
    path('send-request/', send_request, name='send-request'),
<<<<<<< Updated upstream
    path('block-user/', block_user, name='block-user'),
    path('withdraw-request/', withdraw_send_request, name='withdraw-request')

=======
    path('withdraw-request/', withdraw_send_request, name='withdraw-request'),
>>>>>>> Stashed changes
]

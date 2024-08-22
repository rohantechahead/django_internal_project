from django.urls import path

from user_connection.views import handle_friend_request,send_request, block_user, withdraw_send_request,report_user

urlpatterns = [

    path('accept-reject/', handle_friend_request, name='accept-reject'),
    path('send-request/', send_request, name='send-request'),
    path('block-user/', block_user, name='block-user'),
    path('withdraw-request/', withdraw_send_request, name='withdraw-request'),
    path('report-user/',report_user,name='report_user')
]

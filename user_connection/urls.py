from django.urls import path


from user_connection.views import send_request, withdraw_send_request, list_connection

urlpatterns = [
    path('send-request/', send_request, name='send-request'),
    path('withdraw-request/', withdraw_send_request, name='withdraw-request'),
    path('list_connection/', list_connection, name='list_connection')

]

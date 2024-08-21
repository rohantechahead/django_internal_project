from django.urls import path

from user_connection.views import send_request

urlpatterns = [
path('send-request/', send_request, name='send-request'),
]

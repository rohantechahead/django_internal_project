from django.urls import path

from user_connection.views import send_request

urlpatterns = [
    #To be done  # path('demo/', index_page, name='signup')
path('send-request/', send_request, name='send-request'),
]

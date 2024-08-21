from django.urls import path

from user_connection.views import handle_friend_request

urlpatterns = [

    path('accept-reject/', handle_friend_request, name='accept-reject')
]

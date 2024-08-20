from django.urls import path

from user_connection.views import index_page

urlpatterns = [
    #To be done
    path('demo/', index_page, name='signup')
]

from django.urls import path
from user_notification.views import index, list_notifications, create_notification, mark_as_read

urlpatterns = [
    path('', index, name='notification'),
    path('list/', list_notifications, name='list_notifications'),
    path('create/', create_notification, name='create_notification'),
    path('read/<int:notification_id>/', mark_as_read, name='mark_as_read'),
]

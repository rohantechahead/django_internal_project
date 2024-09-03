from django.urls import path
from user_notification.views import index, list_notifications,  mark_as_read

urlpatterns = [
    path('', index, name='notification'),
    path('notification-list/', list_notifications,name='list_notifications'),
    path('read/<int:notification_id>/', mark_as_read, name='mark_as_read'),
]

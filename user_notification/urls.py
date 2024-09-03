from django.urls import path
from user_notification.views import index, notification_list, mark_notification_as_read_or_delete

urlpatterns = [
    path('', index, name='notification'),
    path('list/', notification_list, name='list_notifications'),
    path('notification/<int:notification_id>/<str:action>/', mark_notification_as_read_or_delete, name='mark_notification_as_read_or_delete'),
]

from django.http import HttpResponse
from rest_framework import status
from rest_framework.response import Response
from .models import Notification
from .serializers import NotificationSerializer
from rest_framework.decorators import api_view
from utility.authentication_helper import is_auth
def index(request):
    return HttpResponse("Welcome to Notification Page.")
@api_view(['POST'])
@is_auth
def create_notification(request):
    serializer = NotificationSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@is_auth
def mark_as_read(request,notification_id):
    try:
        notification = Notification.objects.get(id=notification_id, receiver=request.user)
        notification.is_read = True
        notification.save()
        serializer = NotificationSerializer(notification)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Notification.DoesNotExist:
        return Response({"error": "Notification not found"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@is_auth
def list_notifications(request):
    user = request.user
    notifications = Notification.objects.filter(receiver=request.user, is_read=False)
    serializer = NotificationSerializer(notifications, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
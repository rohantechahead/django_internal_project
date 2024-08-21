from rest_framework import status
from django.shortcuts import render
from rest_framework.response import Response
from User_Auth.models import User
from utility.authentication_helper import is_auth
from .validators import verifying_user_connection_request
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from .models import UserConnection, BlockedUser
from utility.api_documantion_helper import block_user_api_doc
from .serializers import UserConnectionSerializer, BlockedUserSerializer


@api_view(['POST'])
@is_auth
def send_request(request):
    if not verifying_user_connection_request(request):
        return Response({"Message": "User not verified"}, status=status.HTTP_400_BAD_REQUEST)

    user_id = request.user_id

    sender = User.objects.get(id=user_id)
    receiver_id = request.data.get('receiver_id')

    try:
        receiver_id = int(receiver_id)
    except ValueError:
        return Response({"error": "Invalid receiver_id format"}, status=status.HTTP_400_BAD_REQUEST)

    receiver = User.objects.filter(id=receiver_id).first()

    if not receiver:
        return Response({"error": "Receiver not found"}, status=status.HTTP_404_NOT_FOUND)

    # Check if the connection request already exists
    if UserConnection.objects.filter(sender_id=sender, receiver_id=receiver).exists():
        return Response({"error": "Request already sent"}, status=status.HTTP_400_BAD_REQUEST)

    # Create the connection request
    connection = UserConnection.objects.create(sender_id=sender, receiver_id=receiver)
    serializer = UserConnectionSerializer(connection)

    return Response({"message": "Request sent successfully", "data": serializer.data}, status=status.HTTP_201_CREATED)


@block_user_api_doc
@api_view(['POST'])
@is_auth
def block_user(request):
    user_id = request.user_id
    blocked_user_id = request.data.get('blocked_user_id')

    try:
        blocked_user_id = int(blocked_user_id)
    except ValueError:
        return Response({"error": "value is not a valid integer, give correct blocked_user_id"},
                        status=status.HTTP_400_BAD_REQUEST)

    blocked_user = User.objects.filter(id=blocked_user_id).first()

    if not blocked_user:
        return Response({"error": "User blocked does not exist"}, status=status.HTTP_404_NOT_FOUND)

    if BlockedUser.objects.filter(blocker_id=user_id, blocked_id=blocked_user_id).exists():
        return Response({"error": "User is already blocked"}, status=status.HTTP_400_BAD_REQUEST)

    block_entry = BlockedUser.objects.create(blocker_id=user_id, blocked_id=blocked_user_id)
    serializer = BlockedUserSerializer(block_entry)

    return Response({"message": "User blocked successfully", "data": serializer.data}, status=status.HTTP_201_CREATED)

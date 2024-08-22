from django.db.models import Q
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from User_Auth.models import User
from utility.api_documantion_helper import send_request_api_doc, withdraw_send_request_api_doc, list_connection_api_doc
from utility.authentication_helper import is_auth
from .models import UserConnection
from .serializers import UserConnectionSerializer
from .validators import verifying_user_connection_request


@send_request_api_doc
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

    if UserConnection.objects.filter(sender_id=sender, receiver_id=receiver).exists():
        return Response({"error": "Request already sent"}, status=status.HTTP_400_BAD_REQUEST)

    connection = UserConnection.objects.create(sender_id=sender, receiver_id=receiver)
    serializer = UserConnectionSerializer(connection)

    return Response({"message": "Request sent successfully", "data": serializer.data}, status=status.HTTP_201_CREATED)


@withdraw_send_request_api_doc
@api_view(['POST'])
@is_auth
def withdraw_send_request(request):
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

    connection = UserConnection.objects.filter(sender_id=sender, receiver_id=receiver)
    connection.delete()
    return Response({"message": "Request Withdrawn successfully"}, status=status.HTTP_200_OK)


@list_connection_api_doc
@api_view(['GET'])
@is_auth
def list_connection(request):
    user_id = request.user_id

    connections = UserConnection.objects.filter(Q(sender_id=user_id) | Q(receiver_id=user_id))

    if not connections.exists():
        return Response({"message": "No connection requests found"}, status=status.HTTP_404_NOT_FOUND)
    serializer = UserConnectionSerializer(connections, many=True)

    return Response({"message": "Connection requests fetched successfully", "data": serializer.data},
                    status=status.HTTP_200_OK)

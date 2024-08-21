from rest_framework import status
<<<<<<< Updated upstream
from rest_framework.decorators import api_view
from rest_framework.response import Response

from User_Auth.models import User
from utility.api_documantion_helper import send_request_api_doc, withdraw_send_request_api_doc,block_user_api_doc
from utility.authentication_helper import is_auth
from utility.email_utils import send_email
from .models import UserConnection, BlockedUser
from .serializers import UserConnectionSerializer, BlockedUserSerializer
from .validators import verifying_user_connection_request
=======
from django.shortcuts import render
from rest_framework.response import Response
from User_Auth.models import User
from utility.api_documantion_helper import send_request_api_doc, withdraw_send_request_api_doc,accept_reject_api_doc
from utility.authentication_helper import is_auth
from utility.email_utils import send_email
from.validators import verifying_user_connection_request,verifying_accept_reject_request
from rest_framework.decorators import api_view
from.models import UserConnection
from.serializers import UserConnectionSerializer
>>>>>>> Stashed changes


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

    # Check if the connection request already exists
    if UserConnection.objects.filter(sender_id=sender, receiver_id=receiver).exists():
        return Response({"error": "Request already sent"}, status=status.HTTP_400_BAD_REQUEST)

    # Create the connection request
    connection = UserConnection.objects.create(sender_id=sender, receiver_id=receiver)
    serializer = UserConnectionSerializer(connection)

    subject = "New Friend Request"
    plain_text_body = "You have received a new friend request."
    html_template_path = "friend_request_email.html"
    context = {
        "recipient_name": receiver.username,
        "sender_name": sender.username,
        "accept_request_link": "https://example.com/accept-request"
    }
    to_email = receiver.email
    send_email(subject, plain_text_body, html_template_path, context, to_email)

    return Response({"message": "Request sent successfully", "data": serializer.data}, status=status.HTTP_201_CREATED)


<<<<<<< Updated upstream
@send_request_api_doc
@api_view(['POST'])
@is_auth
def send_request(request):
    if not verifying_user_connection_request(request):
        return Response({"Message": "User not verified"}, status=status.HTTP_400_BAD_REQUEST)

    user_id = request.user_id
=======
@accept_reject_api_doc
@api_view(['POST'])
@is_auth
def handle_friend_request(request):
    if not verifying_accept_reject_request(request):
        return Response({"Message": "User not verified"}, status=status.HTTP_400_BAD_REQUEST)
    sender_id = request.data.get('sender_id')
    action = request.data.get('action')
    user_id = request.user_id

    if action not in ['accept', 'reject']:
        return Response({"error": "Invalid action"}, status=status.HTTP_400_BAD_REQUEST)

    connection = UserConnection.objects.filter(sender_id=sender_id,
                                               receiver_id=user_id,
                                               status=UserConnection.Status.PENDING).first()
    if not connection:
        return Response({"error": "Connection request not found."}, status=status.HTTP_404_NOT_FOUND)

    if action == 'accept':
>>>>>>> Stashed changes

    sender = User.objects.get(id=user_id)
    receiver_id = request.data.get('receiver_id')

<<<<<<< Updated upstream
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

    subject = "New Friend Request"
    plain_text_body = "You have received a new friend request."
    html_template_path = "friend_request_email.html"
    context = {
        "recipient_name": receiver.username,
        "sender_name": sender.username,
        "accept_request_link": "https://example.com/accept-request"
    }
    to_email = receiver.email
    send_email(subject, plain_text_body, html_template_path, context, to_email)
    return Response({"message": "Request sent successfully", "data": serializer.data}, status=status.HTTP_201_CREATED)
=======
        return Response({"status": "success", "message": "Connection request accepted. You are now connected."})

    elif action == 'reject':
        connection.delete()

        return Response({"status": "success", "message": "Connection request rejected."})
>>>>>>> Stashed changes


@withdraw_send_request_api_doc
@api_view(['POST'])
@is_auth
def withdraw_send_request(request):
    if not verifying_user_connection_request(request):
<<<<<<< Updated upstream
        return Response({"Message": "User not verified"}, status=status.HTTP_400_BAD_REQUEST)

    user_id = request.user_id
=======
        return Response({"Message":"User not verified"},status=status.HTTP_400_BAD_REQUEST)

    user_id=request.user_id
>>>>>>> Stashed changes

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
<<<<<<< Updated upstream


@block_user_api_doc
@api_view(['POST'])
@is_auth
def block_user(request):
    user_id = request.user_id
    blocked_user_id = request.data.get('blocked_user_id')
=======
>>>>>>> Stashed changes

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

    block_entry = BlockedUser.objects.create(blocker_id_id=user_id, blocked_id_id=blocked_user_id)
    serializer = BlockedUserSerializer(block_entry)

    return Response({"message": "User blocked successfully", "data": serializer.data}, status=status.HTTP_201_CREATED)

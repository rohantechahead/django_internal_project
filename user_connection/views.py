from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from User_Auth.models import User
from user_wish.validators import verifying_user_request
from utility.api_documantion_helper import send_request_api_doc, withdraw_send_request_api_doc,accept_reject_api_doc,block_user_api_doc, report_user_api_doc
from utility.authentication_helper import is_auth
from utility.email_utils import send_email
from .models import UserConnection, BlockedUser, ReportedUser
from .serializers import UserConnectionSerializer, BlockedUserSerializer, ReportedUserSerializer
from .validators import verifying_user_connection_request,verifying_accept_reject_request, verifying_user_report


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


@accept_reject_api_doc
@api_view(['POST'])
@is_auth
def handle_friend_request(request):
    if not verifying_accept_reject_request(request):
        return Response({"Message": "User not verified"}, status=status.HTTP_400_BAD_REQUEST)
    sender_id = request.data.get('sender_id')
    action = request.data.get('action')
    user_id = request.user_id

    connection = UserConnection.objects.filter(sender_id=sender_id,receiver_id=user_id,status=UserConnection.Status.PENDING).first()


    if not connection:
        return Response({"error": "Connection request not found."}, status=status.HTTP_404_NOT_FOUND)

    if action == 'accept':

        connection.status = UserConnection.Status.APPROVED
        connection.save()

        return Response({"status": "success", "message": "Connection request accepted. You are now connected."})

    elif action == 'reject':
        connection.delete()

        return Response({"status": "success", "message": "Connection request rejected."})


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

    block_entry = BlockedUser.objects.create(blocker_id_id=user_id, blocked_id_id=blocked_user_id)
    serializer = BlockedUserSerializer(block_entry)

    return Response({"message": "User blocked successfully", "data": serializer.data}, status=status.HTTP_201_CREATED)


@report_user_api_doc
@api_view(['POST'])
@is_auth
def report_user(request):
    is_valid, errors = verifying_user_report(request)
    if not is_valid:
        return Response({"errors": errors}, status=status.HTTP_400_BAD_REQUEST)

    user_id = request.user_id
    reported_user_id = request.data.get('reported_user_id')
    reason = request.data.get('reason')

    try:
        reported_user_id = int(reported_user_id)
    except ValueError:
        return Response({"error": "Reported user id must be a valid integer"}, status=status.HTTP_400_BAD_REQUEST)

    if not reason:
        return Response({"error": "Reason for reporting is required"}, status=status.HTTP_400_BAD_REQUEST)

    reported_user = User.objects.filter(id=reported_user_id).first()
    if not reported_user:
        return Response({"error": "User does not exist"}, status=status.HTTP_404_NOT_FOUND)

    # Check if the user has already reported
    if ReportedUser.objects.filter(reporter_id=user_id, reported_id=reported_user_id).exists():
        return Response({"error": "You have already reported this user"}, status=status.HTTP_400_BAD_REQUEST)

    # Create the report entry
    report_entry = ReportedUser.objects.create(reporter_id_id=user_id, reported_id_id=reported_user_id, reason=reason)
    serializer = ReportedUserSerializer(report_entry)

    return Response({"message": "User reported successfully", "data": serializer.data}, status=status.HTTP_201_CREATED)
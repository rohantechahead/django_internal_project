from django.contrib.auth.hashers import make_password
from django.db.models import Q
from rest_framework import status, generics
from rest_framework.decorators import api_view
from rest_framework.response import Response

from utility.api_documantion_helper import (login_api_doc, signup_api_doc, forgot_api_doc,
                                            update_security_api_doc, get_security_api_doc, logout_api_doc,
                                            update_profile_api_doc, get_profile_api_doc,
                                            user_delete_api_doc, get_refresh_token_api_doc)
from utility.authentication_helper import generate_refresh_token, generate_access_token, is_auth

from utility.email_utils import send_email
from .models import User, UsersecurityQuestion
from .serializer import LoginSerializer, UserProfileSerializer, UserSerializer
from .validator import verifying_user_login, verifying_signup_request, verifying_forgotpassword_request, \
    verifying_refresh_token

from utility.common_message import CommonMessage


@signup_api_doc
@api_view(['POST'])
def signup_api(request):
    # Validate the signup request
    if not verifying_signup_request(request):
        return Response({"Error": "Invalid request body"}, status=status.HTTP_400_BAD_REQUEST)

    # Extract security question and answer
    security_q = request.data.get('security_q')
    security_a = request.data.get('security_a')

    # Check if security question and answer are provided
    if not security_q or not security_a:
        return Response({"Error": "Security question and answer are required"}, status=status.HTTP_400_BAD_REQUEST)

    # Extract username and email
    username = request.data.get('username')
    email = request.data.get('email')

    # Create the user
    user = User(username=username, email=email)
    user.set_password(request.data.get('password'))

    # If email is not provided, use a default email
    if not email:
        user.email = f"{username}@yopmail.com"

    # Save the user to the database
    user.save()

    # Save the security question and answer after the user is created
    user_security_q = UsersecurityQuestion(user_id=user, security_q=security_q, security_a=security_a)
    user_security_q.save()

    return Response({"Success": CommonMessage.SIGNUP_REQUEST_SUCCESS}, status=status.HTTP_200_OK)


@login_api_doc
@api_view(['POST'])
def user_login(request):
    if not verifying_user_login(request):
        return Response({'success': False, 'message': 'Invalid data'}, status=400)
    username_or_email = request.data.get('username')
    password = request.data.get('password')
    if not username_or_email or not password:
        return Response({'error': CommonMessage.REQUIRED_UNAME_PASSWORD}, status=status.HTTP_400_BAD_REQUEST)
    try:
        user = User.objects.get(Q(username=username_or_email) | Q(email=username_or_email))
    except User.DoesNotExist:
        return Response({'error':CommonMessage.INVALID_CREDENTIAL }, status=status.HTTP_401_UNAUTHORIZED)
    if not user.check_password(password):
        return Response({'error': CommonMessage.INCORRECT_PASS}, status=status.HTTP_401_UNAUTHORIZED)
    if user.is_block:
        return Response({"message": CommonMessage.ADMIN_BLOCK_USER}, status=status.HTTP_403_FORBIDDEN)
    access_token = generate_access_token(user)
    refresh_token = generate_refresh_token(user)

    user_data = LoginSerializer(user).data
    user_data.update({
        "access_token": access_token,
        "refresh_token": refresh_token

    })
    user.refresh_token = str(refresh_token)
    user.is_login = True

    user.save()
    return Response(user_data, status=status.HTTP_200_OK)


@forgot_api_doc
@api_view(['POST'])
def forgot_password_api(request):
    if not verifying_forgotpassword_request(request):
        return Response({'success': False, 'message': 'Invalid data'}, status=400)
    username_or_email = request.data.get('username')
    security_q = request.data.get('security_q')
    security_a = request.data.get('security_a')
    new_password = request.data.get('new_password')

    try:
        user = User.objects.get(Q(username=username_or_email) | Q(email=username_or_email))
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    try:
        user_security_q = UsersecurityQuestion.objects.get(user_id=user)
    except UsersecurityQuestion.DoesNotExist:
        return Response({'error': 'Security question not found'}, status=status.HTTP_404_NOT_FOUND)

    if user_security_q.security_q != security_q or user_security_q.security_a != security_a:
        return Response({'error': 'Security question or answer is incorrect'}, status=status.HTTP_401_UNAUTHORIZED)

    user.set_password(new_password)
    user.save()

    return Response({'success': True, 'message': CommonMessage.PASSWORD_RESET_SUCCESS}, status=status.HTTP_200_OK)


@update_security_api_doc
@api_view(['PUT'])
@is_auth
def update_security_q_a(request):
    user_id = request.user_id
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    security_q = request.data.get('security_q')
    security_a = request.data.get('security_a')

    if not security_q or not security_a:
        return Response({'error': 'Both security question and answer are required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user_security_q = UsersecurityQuestion.objects.get(user_id=user)
        user_security_q.security_q = security_q
        user_security_q.security_a = make_password(security_a)
        user_security_q.save()

        return Response({'success': True, 'message': CommonMessage.UPDATE_SECURITY_Q_A},
                        status=status.HTTP_200_OK)
    except UsersecurityQuestion.DoesNotExist:
        return Response({'error': 'Security question not found'}, status=status.HTTP_404_NOT_FOUND)


@get_security_api_doc
@api_view(['GET'])
@is_auth
def get_security_q_a(request):
    user_id = request.user_id

    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    try:
        user_security_q = UsersecurityQuestion.objects.get(user_id=user)
    except UsersecurityQuestion.DoesNotExist:
        return Response({'error': 'Security question not found'}, status=status.HTTP_404_NOT_FOUND)

    data = {
        'security_q': user_security_q.security_q,
        'security_a': user_security_q.security_a,
    }
    return Response(data, status=status.HTTP_200_OK)


@update_profile_api_doc
@api_view(['PUT'])
@is_auth
def update_profile(request):
    user_id = request.user_id
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({"Error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    username = user.username
    email = request.data.get('email')
    if email:
        user.email = email
    else:

        user.email = f"{username}@yopmal.com"

    user.first_name = request.data.get('first_name')
    user.last_name = request.data.get('last_name')

    user.gender = request.data.get('gender')

    user.dob = request.data.get('dob')
    user.phone_no = request.data.get('phone_no')
    user.save()

    return Response({"Success": CommonMessage.UPDATE_PROFILE_SUCCESS}, status=status.HTTP_200_OK)


@logout_api_doc
@api_view(['POST'])
@is_auth
def user_logout(request):
    try:
        # Retrieve the authenticated user's ID from the request object
        user_id = request.user_id

        # Fetch the user instance from the database using the user_id
        user = User.objects.get(id=user_id)

        # Clear the user's tokens to effectively log them out
        user.refresh_token = ""
        user.is_login = False
        # Save the updated user instance to the database
        user.save()
        return Response({'success': True, 'message': CommonMessage.USER_LOGOUT_SUCCESS}, status=status.HTTP_200_OK)

    except User.DoesNotExist:
        return Response({'success': False, 'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        return Response({'success': False, 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        user_id = request.user_id
        user = User.objects.get(id=user_id)
        user.refresh_token = ""
        user.is_login = False
        user.save()
        return Response({'success': True, 'message': SuccessMessage.USER_LOGOUT_SUCCESS}, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({'success': False, 'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'success': False, 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@get_profile_api_doc
@api_view(['GET'])
@is_auth
def get_profile(request):
    user_id = request.user_id
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({"Error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
    serializer = UserProfileSerializer(user)
    return Response(serializer.data, status=status.HTTP_200_OK)


@user_delete_api_doc
@api_view(['DELETE'])
@is_auth
def user_delete(request):
    try:
        user_id = request.user_id
        user = User.objects.get(id=user_id)
        user.delete()
        return Response({'success': True, 'message': CommonMessage.USER_DELETE_SUCCESS}, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({'success': False, 'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'success': False, 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@get_refresh_token_api_doc
@api_view(['POST'])
def get_refresh_token(request):
    if not verifying_refresh_token(request):
        return Response({"Error": "Invalid Request Body"}, status=status.HTTP_400_BAD_REQUEST)
    refresh_token = request.data.get('refresh_token')
    user = User.objects.get(refresh_token=refresh_token)
    new_refresh_token = generate_refresh_token(user)
    access_token = generate_access_token(user)
    if refresh_token:
        user.refresh_token = new_refresh_token
    user.save()
    return Response({"refresh_token": new_refresh_token,
                     "access_token": access_token}, status=status.HTTP_200_OK)


@api_view(['POST'])
def send_test_email(request):
    subject = "New Friend Request"
    plain_text_body = "You have received a new friend request."
    html_template_path = "friend_request_email.html"  # Updated path
    context = {
        "recipient_name": "John Doe",
        "sender_name": "Jane Smith",
        "accept_request_link": "https://example.com/accept-request"
    }
    to_email = "afzal@yopmail.com"
    send_email(subject, plain_text_body, html_template_path, context, to_email)

    return Response({"Success": CommonMessage.SEND_EMAIL_SUCCESS}, status=status.HTTP_200_OK)






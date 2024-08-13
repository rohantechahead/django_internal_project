from functools import wraps

from django.contrib.auth.hashers import make_password
from django.db.models import Q
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from utility.authentication_helper import generate_refresh_token, generate_access_token
from .models import User,UsersecurityQuestion
from .serializer import LoginSerializer
from .validator import verifying_user_login, verifying_signup_request, verifying_forgotpassword_request


from utility.authentication_helper import generate_refresh_token, generate_access_token, is_auth
from .models import User
from .serializer import LoginSerializer
from .validator import verifying_user_login, verifying_signup_request
from rest_framework.permissions import IsAuthenticated



@api_view(['POST'])
def signup_api(request):
    if not verifying_signup_request(request):
       return Response({"Error": "Invalid request body"}, status=status.HTTP_400_BAD_REQUEST)
    security_q = request.data.get('security_q')
    security_a = request.data.get('security_a')

    if not security_q or not security_a:
        return Response({"Error": "Security question and answer are required"}, status=status.HTTP_400_BAD_REQUEST)

    # # Create the user
    user = User(username=request.data.get('username'))


    user.set_password(request.data.get('password'))
    user.save()

    user_security_q = UsersecurityQuestion(user_id=user, security_q=security_q, security_a=security_a)
    user_security_q.save()



    # Get the username from the request
    username = request.data.get('username')
    email = request.data.get('email')

    # Create the user
    if not email:
        user.email = f"{username}@yopmal.com"

    user.save()

    return Response({"Success": "User Created Successfully"}, status=status.HTTP_200_OK)


@api_view(['POST'])
def user_login(request):
    if not verifying_user_login(request):
        return Response({'success': False, 'message': 'Invalid data'}, status=400)
    username_or_email = request.data.get('username')
    password = request.data.get('password')

    if not username_or_email or not password:
        return Response({'error': 'Username and password are required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = User.objects.get(Q(username=username_or_email) | Q(email=username_or_email))
    except User.DoesNotExist:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    user.save()
    if not user.check_password(password):
        return Response({'error': 'Incorrect password'}, status=status.HTTP_401_UNAUTHORIZED)

    access_token = generate_access_token(user)
    refresh_token = generate_refresh_token(user)

    user_data = LoginSerializer(user).data
    user_data.update({
        "access_token": access_token,
        "refresh_token": refresh_token
    })
    user.refresh_token=str(refresh_token)
    user.is_login=True

    user.save()
    return Response(user_data, status=status.HTTP_200_OK)

@api_view(['POST'])
def forgot_password_api(request):
    if not verifying_forgotpassword_request(request):
        return Response({'success': False, 'message': 'Invalid data'}, status=400)
    username_or_email = request.data.get('username')
    security_q=request.data.get('security_q')
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

    return Response({'success': True, 'message': 'Password reset successfully'}, status=status.HTTP_200_OK)


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

        return Response({'success': True, 'message': 'Security question and answer updated successfully'}, status=status.HTTP_200_OK)
    except UsersecurityQuestion.DoesNotExist:
        return Response({'error': 'Security question not found'}, status=status.HTTP_404_NOT_FOUND)


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


@api_view(['PUT'])
@is_auth
def update_profile(request):
    user_id = request.user_id
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({"Error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    username=user.username

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

    return Response({"Success": "Profile Updated Successfully"}, status=status.HTTP_200_OK)


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
        user.is_login=False
        # Save the updated user instance to the database
        user.save()
        return Response({'success': True, 'message': 'Logged out successfully'}, status=status.HTTP_200_OK)

    except User.DoesNotExist:
        return Response({'success': False, 'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        return Response({'success': False, 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


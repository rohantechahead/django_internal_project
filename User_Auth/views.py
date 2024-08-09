from django.db.models import Q
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from utility.authentication_helper import generate_refresh_token, generate_access_token
from .models import User
from .serializer import LoginSerializer
from .validator import verifying_user_login, verifying_signup_request


@api_view(['POST'])
def signup_api(request):
    if not verifying_signup_request(request):
        return Response({"Error": "Invalid request body"}, status=status.HTTP_400_BAD_REQUEST)

    # Create the user
    user = User(username=request.data.get('username'))
    user.set_password(request.data.get('password'))
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

    if not user.check_password(password):
        return Response({'error': 'Incorrect password'}, status=status.HTTP_401_UNAUTHORIZED)

    access_token = generate_access_token(user)
    refresh_token = generate_refresh_token(user)

    user_data = LoginSerializer(user).data
    user_data.update({
        "access_token": access_token,
        "refresh_token": refresh_token
    })

    return Response(user_data, status=status.HTTP_200_OK)


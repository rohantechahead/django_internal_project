from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import User
from .serializer import LoginSerializer
from .validator import verifying_user_login,verifying_signup_request


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
def login(request):
    # Validate the incoming data using Cerberus
    if not verifying_user_login(request):
        return Response({'success': False, 'message': 'Invalid data'}, status=400)

    # If validation passes, check if user exists
    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')

    try:
        if username:
            user = User.objects.get(username=username, password=password)
        else:
            user = User.objects.get(email=email, password=password)

        # Here, you can generate tokens or start a session
        return Response({'success': True, 'message': 'Login successful'})

    except User.DoesNotExist:
        return Response({'success': False, 'message': 'Invalid credentials'}, status=400)




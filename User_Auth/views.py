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



@api_view(['POST'])
def signup_api(request):
    if not verifying_signup_request(request):
       return Response({"Error": "Invalid request body"}, status=status.HTTP_400_BAD_REQUEST)
    security_q = request.data.get('security_q')
    security_a = request.data.get('security_a')

<<<<<<< HEAD
    if not security_q or not security_a:
        return Response({"Error": "Security question and answer are required"}, status=status.HTTP_400_BAD_REQUEST)

    # # Create the user
    user = User(username=request.data.get('username'))


    user.set_password(request.data.get('password'))
    user.save()

    user_security_q = UsersecurityQuestion(user_id=user, security_q=security_q, security_a=security_a)
    user_security_q.save()

=======
    # Get the username from the request
    username = request.data.get('username')
    email = request.data.get('email')



    # Create the user
    user = User(username=username, email=email)
    user.set_password(request.data.get('password'))
    # Set the email as username + '@yopmal.com'
    if not email:
        user.email = f"{username}@yopmal.com"

    user.save()
>>>>>>> ebd5a48612a96cfee1b11836c2ba6a719071574a
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
<<<<<<< HEAD

@api_view(['POST'])
def forgot_password_api(request):
    if not verifying_forgotpassword_request(request):
        return Response({'success': False, 'message': 'Invalid data'}, status=400)
    username_or_email = request.data.get('username_or_email')
    security_q = request.data.get('security_q')
    security_a = request.data.get('security_a')
    # new_password = request.data.get('new_password')

    try:
        user = User.objects.get(Q(username=username_or_email) | Q(email=username_or_email))
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    try:
        user_security_q = UsersecurityQuestion.objects.get(user_id=user.id)
    except UsersecurityQuestion.DoesNotExist:
        return Response({'error': 'Security question not found'}, status=status.HTTP_404_NOT_FOUND)

    if user_security_q.security_q != security_q or user_security_q.security_a != security_a:
        return Response({'error': 'Security question or answer is incorrect'}, status=status.HTTP_401_UNAUTHORIZED)

    new_password = 'newpassword'
    user.set_password(new_password)
    user.save()

    return Response({'success': True, 'message': 'Password reset successfully'}, status=status.HTTP_200_OK)

@api_view(['PUT'])
def update_security_q_a(request, user_id):
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    security_question = request.data.get('security_question')
    security_answer = request.data.get('security_answer')

    if not security_question or not security_answer:
        return Response({'error': 'Both security question and answer are required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user_security_q = UsersecurityQuestion.objects.get(user_id=user)
        user_security_q.security_question = security_question
        user_security_q.security_answer = make_password(security_answer)
        user_security_q.save()

        return Response({'success': True, 'message': 'Security question and answer updated successfully'}, status=status.HTTP_200_OK)
    except UsersecurityQuestion.DoesNotExist:
        return Response({'error': 'Security question not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['DELETE'])
def delete_security_q_a(request, user_id):
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    try:
        user_security_q = UsersecurityQuestion.objects.get(user_id=user)
        user_security_q.security_question = ''
        user_security_q.security_answer = ''
        user_security_q.save()

        return Response({'success': True, 'message': 'Security question and answer deleted successfully'}, status=status.HTTP_200_OK)
    except UsersecurityQuestion.DoesNotExist:
        return Response({'error': 'Security question not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def get_security_q_a(request, user_id):
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    try:
        user_security_q = UsersecurityQuestion.objects.get(user_id=user)
    except UsersecurityQuestion.DoesNotExist:
        return Response({'error': 'Security question not found'}, status=status.HTTP_404_NOT_FOUND)

    data = {
        'security_question': user_security_q.security_question,
    }
    return Response(data, status=status.HTTP_200_OK)



=======
>>>>>>> ebd5a48612a96cfee1b11836c2ba6a719071574a

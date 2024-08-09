from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import User
from .validator import verifying_signup_request


@api_view(['POST'])
def signup_api(request):
    """
    Handle user signup requests.

    This view function handles POST requests to create a new user. It validates
    the request body using the `verifying_signup_request` function, and if valid,
    creates a new user with the provided username and password.

    Args:
        request (Request): The HTTP request object containing the user data.

    Returns:
        Response: A Response object with a success message and HTTP 200 status if
        the user is created successfully, or an error message and HTTP 400 status
        if the request body is invalid.
    """
    if not verifying_signup_request(request):
        return Response({"Error": "Invalid request body"}, status=status.HTTP_400_BAD_REQUEST)

    # Create the user
    user = User(username=request.data.get('username'))
    user.set_password(request.data.get('password'))
    user.save()

    return Response({"Success": "User Created Successfully"}, status=status.HTTP_200_OK)

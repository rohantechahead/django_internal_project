from functools import wraps

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view
from rest_framework.response import Response


def signup_api_doc(func):
    @swagger_auto_schema(
        method='post',
        operation_description="User create a account",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING, description='Username for the new account'),
                'email': openapi.Schema(type=openapi.TYPE_STRING, description='Email address for the new account'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description='Password for the new account'),
                'security_q': openapi.Schema(type=openapi.TYPE_STRING, description='Security question for the account'),
                'security_a': openapi.Schema(type=openapi.TYPE_STRING, description='Answer to the security question'),
            },
            required=['username', 'password', 'security_q', 'security_a']
        ),
        responses={
            200: openapi.Response(
                description='User Created Successfully',
                examples={
                    'application/json': {
                        'Success': 'User Created Successfully'
                    }
                }
            ),
            400: openapi.Response(
                description='Invalid request body',
                examples={
                    'application/json': {
                        'Error': 'Invalid request body'
                    }
                }
            )
        }
    )
    @wraps(func)
    def wrap(request, *args, **kwargs):
        return func(request, *args, **kwargs)

    return wrap


def login_api_doc(func):
    @swagger_auto_schema(
        method='post',
        operation_description="User login",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING, description='Username or email'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description='Password')
            },
            required=['username', 'password']
        ),
        responses={
            200: openapi.Response(
                description="Login successful",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'access_token': openapi.Schema(type=openapi.TYPE_STRING, description='Access token'),
                        'refresh_token': openapi.Schema(type=openapi.TYPE_STRING, description='Refresh token'),
                        'username': openapi.Schema(type=openapi.TYPE_STRING, description='Username'),
                        'email': openapi.Schema(type=openapi.TYPE_STRING, description='Email')
                    }
                )
            ),
            400: openapi.Response(
                description="Invalid data"
            ),
            401: openapi.Response(
                description="Invalid credentials or incorrect password"
            )
        }
    )
    @wraps(func)
    def wrap(request, *args, **kwargs):
        return func(request, *args, **kwargs)

    return wrap


def logout_api_doc(func):
    @swagger_auto_schema(
        method='post',
        operation_description="User logout",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'refresh_token': openapi.Schema(type=openapi.TYPE_STRING, description='Refresh token')
            },
            required=['refresh_token']
        ),
        manual_parameters=[
            openapi.Parameter(
                'Authorization',
                openapi.IN_HEADER,
                description="Bearer token",
                type=openapi.TYPE_STRING,
                required=True,
            ),
        ],
        responses={
            200: openapi.Response(
                description="Logout successful",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'message': openapi.Schema(type=openapi.TYPE_STRING, description='Success message')
                    }
                ),
                examples={
                    'application/json': {
                        'message': 'Logout successful'
                    }
                }
            ),
            400: openapi.Response(
                description="Invalid data",
                examples={
                    'application/json': {
                        'error': 'Invalid data'
                    }
                }
            ),
            401: openapi.Response(
                description="Authorization Token is missing or invalid",
                examples={
                    'application/json': {
                        'error': 'Authorization Token is missing!'
                    }
                }
            ),
            403: openapi.Response(
                description="Permission denied",
                examples={
                    'application/json': {
                        'error': 'Permission denied'
                    }
                }
            ),
        }
    )
    @wraps(func)
    def wrap(request, *args, **kwargs):
        return func(request, *args, **kwargs)

    return wrap


def forgot_api_doc(func):
    @swagger_auto_schema(
        method='post',
        operation_description="Forgot password",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING, description='Username or email'),
                'security_q': openapi.Schema(type=openapi.TYPE_STRING, description='Security question'),
                'security_a': openapi.Schema(type=openapi.TYPE_STRING, description='Answer to the security question'),
                'new_password': openapi.Schema(type=openapi.TYPE_STRING, description='New password')
            },
            required=['username', 'security_q', 'security_a', 'new_password']
        ),
        responses={
            200: openapi.Response(
                description='Password reset successfully',
                examples={
                    'application/json': {
                        'success': True,
                        'message': 'Password reset successfully'
                    }
                }
            ),
            400: openapi.Response(
                description='Invalid data',
                examples={
                    'application/json': {
                        'success': False,
                        'message': 'Invalid data'
                    }
                }
            ),
            404: openapi.Response(
                description='User or security question not found',
                examples={
                    'application/json': {
                        'error': 'User not found or security question not found'
                    }
                }
            ),
            401: openapi.Response(
                description='Incorrect security question or answer',
                examples={
                    'application/json': {
                        'error': 'Security question or answer is incorrect'
                    }
                }
            )
        }
    )
    @wraps(func)
    def wrap(request, *args, **kwargs):
        return func(request, *args, **kwargs)

    return wrap


def update_security_api_doc(func):
    @swagger_auto_schema(
        method='put',
        operation_description="Update security question and answer",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING, description='Username or email'),
                'security_q': openapi.Schema(type=openapi.TYPE_STRING, description='Security question'),
                'security_a': openapi.Schema(type=openapi.TYPE_STRING, description='Answer to the security question'),
            },
            required=['username', 'security_q', 'security_a']
        ),
        manual_parameters=[
            openapi.Parameter(
                'Authorization',
                openapi.IN_HEADER,
                description="Bearer token",
                type=openapi.TYPE_STRING,
                required=True,
            ),
        ],
        responses={
            200: openapi.Response(
                description='Security question and answer updated successfully',
                examples={
                    'application/json': {
                        'success': True,
                        'message': 'Security question and answer updated successfully'
                    }
                }
            ),
            400: openapi.Response(
                description='Both security question and answer are required',
                examples={
                    'application/json': {
                        'error': 'Both security question and answer are required'
                    }
                }
            ),
            401: openapi.Response(
                description='Authorization token is missing or invalid',
                examples={
                    'application/json': {
                        'error': 'Authorization Token is missing!'
                    }
                }
            ),
            403: openapi.Response(
                description='User does not have permission to update security question',
                examples={
                    'application/json': {
                        'error': 'Permission denied'
                    }
                }
            ),
            404: openapi.Response(
                description='User or security question not found',
                examples={
                    'application/json': {
                        'error': 'User not found'  # Or 'Security question not found' if appropriate
                    }
                }
            ),
            500: openapi.Response(
                description='Internal server error',

            )
        }
    )
    @wraps(func)
    def wrap(request, *args, **kwargs):
        return func(request, *args, **kwargs)

    return wrap


def get_security_api_doc(func):
    @swagger_auto_schema(
        method='get',
        operation_description="Retrieve the security question and answer for the user",
        manual_parameters=[
            openapi.Parameter(
                'Authorization',
                openapi.IN_HEADER,
                description="Bearer token",
                type=openapi.TYPE_STRING,
                required=True,
            ),
        ],
        responses={
            200: openapi.Response(
                description='Security question and answer retrieved successfully',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'security_q': openapi.Schema(type=openapi.TYPE_STRING, description='Security question'),
                        'security_a': openapi.Schema(type=openapi.TYPE_STRING,
                                                     description='Answer to the security question'),
                    }
                ),
                examples={
                    'application/json': {
                        'security_q': 'What is your mother\'s maiden name?',
                        'security_a': 'Smith'
                    }
                }
            ),
            404: openapi.Response(
                description='User or security question not found',
                examples={
                    'application/json': {
                        'error': 'User not found'
                    }
                }
            ),
            500: openapi.Response(
                description='Internal server error',
                examples={
                    'application/json': {
                        'error': 'An unexpected error occurred'
                    }
                }
            )
        }
    )
    @wraps(func)
    def wrap(request, *args, **kwargs):
        return func(request, *args, **kwargs)

    return wrap


def update_profile_api_doc(func):
    @swagger_auto_schema(
        method='put',
        operation_description="Update user profile information",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING, description='User email'),
                'first_name': openapi.Schema(type=openapi.TYPE_STRING, description='User first name'),
                'last_name': openapi.Schema(type=openapi.TYPE_STRING, description='User last name'),
                'gender': openapi.Schema(type=openapi.TYPE_STRING, description='User gender'),
                'dob': openapi.Schema(type=openapi.TYPE_STRING, description='User date of birth',
                                      format=openapi.FORMAT_DATE),
                'phone_no': openapi.Schema(type=openapi.TYPE_STRING, description='User phone number'),
            },
            required=['first_name', 'last_name', 'gender', 'dob', 'phone_no']
        ),
        manual_parameters=[
            openapi.Parameter(
                'Authorization',
                openapi.IN_HEADER,
                description="Bearer token",
                type=openapi.TYPE_STRING,
                required=True,
            ),
        ],
        responses={
            200: openapi.Response(
                description='Profile updated successfully',
                examples={
                    'application/json': {
                        'Success': 'Profile Updated Successfully'
                    }
                }
            ),
            400: openapi.Response(
                description='Invalid input data',
                examples={
                    'application/json': {
                        'error': 'Invalid input data'
                    }
                }
            ),
            401: openapi.Response(
                description='Authorization Token is missing or invalid',
                examples={
                    'application/json': {
                        'error': 'Authorization Token is missing!'
                    }
                }
            ),
            404: openapi.Response(
                description='User not found',
                examples={
                    'application/json': {
                        'error': 'User not found'
                    }
                }
            ),
            500: openapi.Response(
                description='Internal server error',
                examples={
                    'application/json': {
                        'error': 'An unexpected error occurred'
                    }
                }
            ),
        }
    )
    @wraps(func)
    def wrap(request, *args, **kwargs):
        return func(request, *args, **kwargs)

    return wrap


def get_profile_api_doc(func):
    @swagger_auto_schema(
        method='get',
        operation_description="Retrieve user profile information",
        manual_parameters=[
            openapi.Parameter(
                'Authorization',
                openapi.IN_HEADER,
                description="Bearer token",
                type=openapi.TYPE_STRING,
                required=True,
            ),
        ],
        responses={
            200: openapi.Response(
                description='User profile retrieved successfully',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'id': openapi.Schema(type=openapi.TYPE_INTEGER, description='User ID'),
                        'username': openapi.Schema(type=openapi.TYPE_STRING, description='Username'),
                        'email': openapi.Schema(type=openapi.TYPE_STRING, description='User email'),
                        'first_name': openapi.Schema(type=openapi.TYPE_STRING, description='User first name'),
                        'last_name': openapi.Schema(type=openapi.TYPE_STRING, description='User last name'),
                        'gender': openapi.Schema(type=openapi.TYPE_STRING, description='User gender'),
                        'dob': openapi.Schema(type=openapi.TYPE_STRING, description='User date of birth',
                                              format=openapi.FORMAT_DATE),
                        'phone_no': openapi.Schema(type=openapi.TYPE_STRING, description='User phone number'),
                        'created_at': openapi.Schema(type=openapi.TYPE_STRING, description='Account creation date',
                                                     format=openapi.FORMAT_DATETIME),
                        'updated_at': openapi.Schema(type=openapi.TYPE_STRING, description='Last update date',
                                                     format=openapi.FORMAT_DATETIME),
                    }
                ),
            ),
            401: openapi.Response(
                description='Unauthorized or invalid token',
                examples={
                    'application/json': {
                        'error': 'Authorization Token is missing or invalid'
                    }
                }
            ),
            404: openapi.Response(
                description='User not found',
                examples={
                    'application/json': {
                        'error': 'User not found'
                    }
                }
            ),
            500: openapi.Response(
                description='Internal server error',
                examples={
                    'application/json': {
                        'error': 'An unexpected error occurred'
                    }
                }
            )
        }
    )
    @wraps(func)
    def wrap(request, *args, **kwargs):
        return func(request, *args, **kwargs)

    return wrap


def user_delete_api_doc(func):
    @swagger_auto_schema(
        method='delete',
        operation_description="Delete a user account",
        manual_parameters=[
            openapi.Parameter(
                'Authorization',
                openapi.IN_HEADER,
                description="Bearer token",
                type=openapi.TYPE_STRING,
                required=True,
            ),
        ],
        responses={
            200: openapi.Response(
                description='User deleted successfully',
                examples={
                    'application/json': {
                        'success': True,
                        'message': 'User deleted successfully'
                    }
                }
            ),
            404: openapi.Response(
                description='User not found',
                examples={
                    'application/json': {
                        'success': False,
                        'error': 'User not found'
                    }
                }
            ),
            500: openapi.Response(
                description='Internal server error',
                examples={
                    'application/json': {
                        'success': False,
                        'error': 'An unexpected error occurred'
                    }
                }
            )
        }
    )
    @wraps(func)
    def wrap(request, *args, **kwargs):
        return func(request, *args, **kwargs)

    return wrap


def get_refresh_token_api_doc(func):
    @swagger_auto_schema(
        method='post',
        operation_description="Retrieve new access and refresh tokens using a refresh token",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'refresh_token': openapi.Schema(type=openapi.TYPE_STRING,
                                                description='The refresh token used to generate new tokens'),
            },
            required=['refresh_token']
        ),
        responses={
            200: openapi.Response(
                description='Successfully generated new tokens',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'refresh_token': openapi.Schema(type=openapi.TYPE_STRING, description='New refresh token'),
                        'access_token': openapi.Schema(type=openapi.TYPE_STRING, description='New access token'),
                    }
                ),
                examples={
                    'application/json': {
                        'refresh_token': 'new_refresh_token_value',
                        'access_token': 'new_access_token_value'
                    }
                }
            ),
            400: openapi.Response(
                description='Invalid request body',
                examples={
                    'application/json': {
                        'Error': 'Invalid Request Body'
                    }
                }
            ),
            401: openapi.Response(
                description='Unauthorized or invalid refresh token',
                examples={
                    'application/json': {
                        'Error': 'Unauthorized or invalid refresh token'
                    }
                }
            ),
            500: openapi.Response(
                description='Internal server error',
                examples={
                    'application/json': {
                        'Error': 'An unexpected error occurred'
                    }
                }
            )
        }
    )
    @wraps(func)
    def wrap(request, *args, **kwargs):
        return func(request, *args, **kwargs)

    return wrap

def send_request_api_doc(func):
    @swagger_auto_schema(
        method='post',
        operation_description="Sending connection request for the user",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'receiver_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='The receiver_id gives us the receivers user_id '),
            },
            required=['receiver_id']
        ),
        manual_parameters=[
            openapi.Parameter(
                'Authorization',
                openapi.IN_HEADER,
                description="Bearer token",
                type=openapi.TYPE_STRING,
                required=True,
            ),
        ],
        responses={
            200: openapi.Response(
                description='Successfully Send Conncetion Request',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'receiver_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='New refresh token'),

                    }
                ),
                examples={
                    'application/json': {
                        'message': 'Request sent Successfully',

                    }
                }
            ),
            400: openapi.Response(
                description='Invalid request body',
                examples={
                    'application/json': {
                        'Error': 'Invalid Request Body'
                    }
                }
            ),
            401: openapi.Response(
                description='Unauthorized or invalid connection request',
                examples={
                    'application/json': {
                        'Error': 'Unauthorized or invalid connection'
                    }
                }
            ),
            500: openapi.Response(
                description='Internal server error',
                examples={
                    'application/json': {
                        'Error': 'An unexpected error occurred'
                    }
                }
            )
        }
    )
    @wraps(func)
    def wrap(request, *args, **kwargs):
        return func(request, *args, **kwargs)

    return wrap

def withdraw_send_request_api_doc(func):
    @swagger_auto_schema(
        method='post',
        operation_description="Withdrawing connection request for the user",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'receiver_id': openapi.Schema(type=openapi.TYPE_INTEGER,description='The receiver_id gives us the receivers user_id '),
            },
            required=['receiver_id']
        ),
        manual_parameters=[
            openapi.Parameter(
                'Authorization',
                openapi.IN_HEADER,
                description="Bearer token",
                type=openapi.TYPE_STRING,
                required=True,
            ),
        ],
        responses={
            200: openapi.Response(
                description='Successfully Withdrawn Conncetion Request',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'receiver_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='New refresh token'),

                    }
                ),
                examples={
                    'application/json': {
                        'message': 'Request Withdrawn Successfully',

                    }
                }
            ),
            400: openapi.Response(
                description='Invalid request body',
                examples={
                    'application/json': {
                        'Error': 'Invalid Request Body'
                    }
                }
            ),
            401: openapi.Response(
                description='Unauthorized or invalid withdrawn request',
                examples={
                    'application/json': {
                        'Error': 'Unauthorized or invalid withdraw request'
                    }
                }
            ),
            500: openapi.Response(
                description='Internal server error',
                examples={
                    'application/json': {
                        'Error': 'An unexpected error occurred'
                    }
                }
            )
        }
    )
    @wraps(func)
    def wrap(request, *args, **kwargs):
        return func(request, *args, **kwargs)

    return wrap

def block_user_api_doc(func):
    @swagger_auto_schema(
        method='post',
        operation_description="Blocked user successfully.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'blocked_user_id': openapi.Schema(type=openapi.TYPE_INTEGER,
                                                  description='block user id for block the user'),
            },
            required=['blocked_user_id']
        ),
        manual_parameters=[
            openapi.Parameter(
                'Authorization',
                openapi.IN_HEADER,
                description="Bearer token",
                type=openapi.TYPE_STRING,
                required=True,
            ),
        ],
        responses={
            200: openapi.Response(
                description='blocked user using blocked user id',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'blocked_user_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='New refresh token'),
                    }
                ),
                examples={
                    'application/json': {
                        'message': 'blocked user successfully',
                    }
                }
            ),
            400: openapi.Response(
                description='Invalid request body',
                examples={
                    'application/json': {
                        'error': 'Invalid Request Body'
                    }
                }
            ),
            404: openapi.Response(
                description='User not found',
                examples={
                    'application/json': {
                        'error': 'User not found'
                    }
                }
            )
        }
    )
    @wraps(func)
    def wrap(request, *args, **kwargs):
        return func(request, *args, **kwargs)

    return wrap


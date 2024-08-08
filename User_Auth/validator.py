from cerberus import Validator


def verifying_signup_request(request):
    # Define the validation schema
    schema = {
        'password': {'type': 'string',  'required': True},
    }
    if "username" in request.data:
        schema.update({'username': {'type': 'string','required': True}})
    else:
        schema.update({'email': {'type': 'string','required': True, 'regex': r'^\S+@\S+\.\S+$'}})

    v = Validator(schema)
    if v.validate(request.data):
        return True
    else:
        return False
# from cerberus import Validator
#
#
# def verifying_signup_request(request):
#     # Define the validation schema
#     schema = {
#         'password': {'type': 'string', 'minlength': 8, 'maxlength': 128, 'required': True},
#     }
#
#     # Conditionally add either 'username' or 'email' to the schema
#     if "username" in request.data:
#         schema.update({'username': {'type': 'string', 'minlength': 3, 'maxlength': 150, 'required': True}})
#     else:
#         schema.update({'email': {'type': 'string', 'maxlength': 254, 'required': True, 'regex': r'^\S+@\S+\.\S+$'}})
#
#
#     v = Validator(schema)
#
#     # Validate the request data
#     if v.validate(request.data):
#         return True
#     else:
#         return False



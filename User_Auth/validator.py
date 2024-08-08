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



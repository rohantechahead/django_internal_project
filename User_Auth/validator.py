from cerberus import Validator
def verifying_signup_request(request):
    # Define the validation schema
    schema = {
        'password': {'type': 'string',  'required': True},
        'username': {'type': 'string','required': True},
        'email':{'type':'string', 'required': False, 'regex': r'^\S+@\S+\.\S+$'}
    }
    # if "username" in request.data:
    #     schema.update({'username': {'type': 'string','required': True}})
    # else:
    #     schema.update({'email': {'type': 'string','required': True, 'regex': r'^\S+@\S+\.\S+$'}})

    v = Validator(schema)
    if v.validate(request.data):
        return True
    else:
        return False
def verifying_user_login(request):
    # Define the validation schema
    schema = {
         # 'username': {'type': 'string', 'minlength': 3, 'maxlength': 150, 'required': True},
         'password': {'type': 'string', 'required': True},
         # 'email': {'type': 'string', 'maxlength': 254, 'required': True, 'regex': r'^\S+@\S+\.\S+$'}
    }
    if "username" in request.data:
        schema.update({'username': {'type': 'string',  'required': True}})
    else:
        schema.update({'email': {'type': 'string',  'required': True, 'regex': r'^\S+@\S+\.\S+$'}})
    v = Validator(schema)

    if v.validate(request.data):
        return True
    else:
        return False




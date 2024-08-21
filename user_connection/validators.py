from cerberus import Validator

def verifying_user_connection_request(request):
    schema = {
        'receiver_id': {'type': 'integer', 'required': True},
    }
    v = Validator()
    if v.validate(request.data, schema):
        return True
    else:
        return False

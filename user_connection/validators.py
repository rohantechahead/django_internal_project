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


def verifying_accept_reject_request(request):
   schema = {
            'sender_id': {'type': 'integer','required': True},
            'action': {'type': 'string','required': True,'allowed': ['accept', 'reject']}
   }
   v = Validator(schema)
   if v.validate(request.data):
       return True
   else:
       return False

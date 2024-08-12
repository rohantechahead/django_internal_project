from rest_framework import serializers

from .models import User, U_security_q


class UserSerializer(serializers.Serializer):
    class Meta:
        model=User
        fields = ('__all__')



class U_security_qSerializer(serializers.ModelSerializer):

    class Meta:
        model = U_security_q
        fields = ['id', 'user_id', 'security_q', 'security_a']

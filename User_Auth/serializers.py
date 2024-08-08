from rest_framework import serializers

from .models import User


class UserSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=200, required=True)

    class Meta:
        model=User
        fields = ('__all__')
        extra_kwargs = {'password': {'write_only': True}}

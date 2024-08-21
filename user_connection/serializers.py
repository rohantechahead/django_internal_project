from rest_framework import serializers
from .models import UserConnection

class UserConnectionSerializer(serializers.ModelSerializer):
    class Meta:
        model=UserConnection
        fields="__all__"



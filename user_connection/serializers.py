from rest_framework import serializers
from .models import UserConnection

class UserConnectionSerializer(serializers.ModelSerializer):
    sender_username = serializers.CharField(source='sender_id.username', read_only=True)
    receiver_username = serializers.CharField(source='receiver_id.username', read_only=True)
    class Meta:
        model = UserConnection
        fields = "__all__"



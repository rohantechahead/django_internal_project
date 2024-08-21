from rest_framework import serializers
from .models import UserConnection, BlockedUser

class UserConnectionSerializer(serializers.ModelSerializer):
    sender_username = serializers.CharField(source='sender_id.username', read_only=True)
    receiver_username = serializers.CharField(source='receiver_id.username', read_only=True)
    class Meta:
        model=UserConnection
        fields="__all__"


class BlockedUserSerializer(serializers.ModelSerializer):
    blocker_username = serializers.CharField(source='blocker.username', read_only=True)
    blocked_username = serializers.CharField(source='blocked.username', read_only=True)

    class Meta:
        model = BlockedUser
        fields = ['id', 'blocker', 'blocker_username', 'blocked', 'blocked_username', 'created_at']
        read_only_fields = ['blocker', 'created_at']
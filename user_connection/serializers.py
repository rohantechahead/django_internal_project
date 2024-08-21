from rest_framework import serializers

from .models import UserConnection

<<<<<<< Updated upstream
from .models import UserConnection, BlockedUser

=======
>>>>>>> Stashed changes

class UserConnectionSerializer(serializers.ModelSerializer):
    sender_username = serializers.CharField(source='sender_id.username', read_only=True)
    receiver_username = serializers.CharField(source='receiver_id.username', read_only=True)

    class Meta:
        model = UserConnection
        fields = "__all__"


    class Meta:
        model = UserConnection
        fields = "__all__"


class BlockedUserSerializer(serializers.ModelSerializer):
    blocker_username = serializers.CharField(source='blocker_id.username', read_only=True)
    blocked_username = serializers.CharField(source='blocked_id.username', read_only=True)

    class Meta:
        model = BlockedUser
        fields = ['id', 'blocker_id', 'blocker_username', 'blocked_id', 'blocked_username', 'created_at']

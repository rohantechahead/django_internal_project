from rest_framework import serializers

from .models import User, UsersecurityQuestion

from .models import User


class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'created_at', 'updated_at']


class UserSerializer(serializers.Serializer):
    class Meta:
        model = User
        # fields = ('__all__')
        fields = ['id', 'username', 'email']

class UsersecurityQuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = UsersecurityQuestion
        fields = ['id', 'user_id', 'security_q', 'security_a']
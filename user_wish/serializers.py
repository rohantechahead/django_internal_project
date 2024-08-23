from rest_framework import serializers
from .models import UserWish


class UserWishSerializers(serializers.ModelSerializer):
    tag_username = serializers.CharField(source='tag_id.username', read_only=True)

    class Meta:
        model=UserWish
        fields="__all__"

    # class Meta:
    #     model = UserWish
    #     fields = ['id', 'title', 'description', 'tag_username']

from rest_framework import serializers
from.models import UserWish

class UserWishSerializers(serializers.ModelSerializer):
    class Meta:
        model=UserWish
        fields="__all__"


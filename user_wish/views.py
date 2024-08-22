from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from User_Auth.models import User
from user_wish.models import UserWish
from user_wish.serializers import UserWishSerializers
from utility.api_documantion_helper import UserWishAddapi_doc
from utility.authentication_helper import is_auth
from .validators import verifying_user_request


# Create your views here.

@UserWishAddapi_doc
@api_view(['POST'])
@is_auth
def UserWishAdd(request):
    if not verifying_user_request(request):
        return Response({"Message": "User not verified"}, status=status.HTTP_400_BAD_REQUEST)

    user_id = request.user_id
    user = User.objects.get(id=user_id)
    title = request.data.get("title")
    description = request.data.get("description")
    tag_id = request.data.get("tag_id")

    tag = User.objects.filter(id=tag_id).first()

    if not tag:
        return Response({"error": "Tag Id not found"}, status=status.HTTP_404_NOT_FOUND)

    if UserWish.objects.filter(userwish_id=user, title=title, description=description, tag_id=tag).exists():
        return Response({"error": "UserWish already created"}, status=status.HTTP_400_BAD_REQUEST)

    connection = UserWish.objects.create(userwish_id=user, title=title, description=description, tag_id=tag)
    serializer = UserWishSerializers(connection)
    return Response({"message": "User Wish created successfully", "data": serializer.data},
                    status=status.HTTP_201_CREATED)

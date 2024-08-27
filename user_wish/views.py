from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from User_Auth.models import User
from user_wish.models import UserWish
from user_wish.serializers import UserWishSerializers
from utility.api_documantion_helper import UserWishAddapi_doc, get_user_wish_api_doc,user_wish_update_api_doc
from utility.authentication_helper import is_auth
from .validators import verifying_user_request, verifying_request
from utility.common_message import CommonMessage


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

    return Response({"message": CommonMessage.USER_WISH_SUCCESS, "data": serializer.data},
                    status=status.HTTP_201_CREATED)

@get_user_wish_api_doc
@api_view(['GET'])
@is_auth
def get_user_wish(request):
    user_id = request.user_id
    user_wish = UserWish.objects.filter(userwish_id=user_id)
    serializer = UserWishSerializers(user_wish, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@user_wish_update_api_doc
@api_view(['PUT'])
@is_auth
def user_wish_update(request,pk):
    if not verifying_request(request):
        return Response({"Message": "User not verified"}, status=status.HTTP_400_BAD_REQUEST)

    user_id = request.user_id
    user_wishes = UserWish.objects.get(userwish_id=user_id,pk=pk)

    updated_title = request.data.get("title")
    updated_description = request.data.get("description")
    user_wishes.title = updated_title
    user_wishes.description = updated_description
    user_wishes.save()

    # Serialize the updated user_wishes
    serializer = UserWishSerializers(user_wishes)


    return Response({"message": CommonMessage.USER_WISH_UPDATE_SUCCESS, "data": serializer.data}, status=status.HTTP_200_OK)


@api_view(['DELETE'])
@is_auth
def user_wish_delete(request,pk):

    user_id = request.user_id
    try:
        user_wishes = UserWish.objects.get(userwish_id=user_id, pk=pk)
    except UserWish.DoesNotExist:
        return Response({"message": "User wish not found"}, status=status.HTTP_404_NOT_FOUND)

    user_wishes.delete()
    return Response({"Message": CommonMessage.USER_WISH_DELETE_SUCCESS},status=status.HTTP_204_NO_CONTENT)



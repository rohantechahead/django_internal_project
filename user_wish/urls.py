from django.urls import path
from user_wish.views import UserWishAdd,get_user_wish

urlpatterns = [
    path('tag-wish/', UserWishAdd, name='tag-wish'),
    path('get-wish/', get_user_wish, name='get-wish'),
]
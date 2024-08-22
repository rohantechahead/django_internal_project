from django.urls import path
from user_wish.views import UserWishAdd

urlpatterns = [
    path('tag-wish/', UserWishAdd, name='tag-wish'),
]
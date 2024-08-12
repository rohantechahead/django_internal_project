from django.db import models
from django.contrib.auth.hashers import check_password, make_password


class User(models.Model):
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50, default=None,blank=True)
    last_name = models.CharField(max_length=50, default=None,blank=True)
    gender = models.CharField(max_length=10, default=None,blank=True)
    DOB = models.CharField(max_length=20, default=None, null=True, blank=True)
    password = models.CharField(max_length=500)
    phone_no = models.IntegerField(default=0,null=True)
    refresh_token = models.CharField(max_length=200, default='None')
    is_login = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

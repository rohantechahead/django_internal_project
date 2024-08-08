from django.contrib.auth.hashers import make_password
from django.db import models


# Create your models here.
class User(models.Model):
    username=models.CharField(max_length=50,unique=True)
    password=models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)




    def set_password(self, raw_password):
        self.password = make_password(raw_password)

# def check_password(self, raw_password):
#     return check_password(raw_password, self.password)
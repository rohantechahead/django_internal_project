from django.db import models
from django.contrib.auth.hashers import check_password


class User(models.Model):
    username=models.CharField(max_length=50,unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=500)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    class Meta:
        # db_table = 'user'
        indexes = [
            models.Index(fields=['username', 'password']),
        ]



from django.db import models
from django.contrib.auth.hashers import check_password, make_password


class User(models.Model):
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)
<<<<<<< HEAD
class UsersecurityQuestion(models.Model):
    id = models.AutoField(primary_key=True, serialize=False)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    security_q = models.CharField(max_length=200)
    security_a = models.CharField(max_length=200)


    def __str__(self):
        return self.security_q

=======
>>>>>>> ebd5a48612a96cfee1b11836c2ba6a719071574a

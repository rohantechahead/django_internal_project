from django.db import models

from User_Auth.models import User


# Create your models here.


class UserConnection(models.Model):
    class Status(models.TextChoices):
        PENDING = 'Pending', 'Request Pending'
        APPROVED = 'Accepted', 'Request Accepted'
        REJECTED = 'Rejected', 'Request Rejected'
        BLOCKED = 'Blocked', 'Blocked'


    status = models.CharField(
        max_length=8,
        choices=Status.choices,
        default=Status.PENDING,
    )
    sender_id = models.ForeignKey(User, on_delete=models.CASCADE,related_name="sent_connections")
    receiver_id = models.ForeignKey(User, on_delete=models.CASCADE,related_name="received_connections")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class BlockedUser(models.Model):
    blocker = models.ForeignKey(User, related_name="blocker", on_delete=models.CASCADE)
    blocked = models.ForeignKey(User, related_name="blocked", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('blocker', 'blocked')
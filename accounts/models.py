from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES = (
         ('OWNER','Owner'),
         ('STAFF','Staff')

    )
    role = models.CharField(max_length=20, choices = ROLE_CHOICES, default = 'user' )
    full_name = models.CharField(max_length=255, blank=True, null=True)


class ActivityLog(models.Model):
    username = models.CharField(max_length=255)
    action = models.CharField(max_length=100) 
    action_details = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.username} - {self.action}"


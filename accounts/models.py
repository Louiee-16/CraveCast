from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES = (
         ('OWNER','Owner'),
         ('STAFF','Staff')

    )
    role = models.CharField(max_length=20, choices = ROLE_CHOICES, default = 'user' )
    full_name = models.CharField(max_length=255, blank=True, null=True)


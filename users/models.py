import uuid
from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class UserProfile(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, unique=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=False, related_name="profile")

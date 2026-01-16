from django.contrib.auth.models import AbstractUser
from django.db import models


def avatar_upload_path(instance, filename: str) -> str:
    return f"avatars/user_{instance.id}/{filename}"


class User(AbstractUser):
    email = models.EmailField(unique=True)
    display_name = models.CharField(max_length=150)
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to=avatar_upload_path, blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'display_name']

    def __str__(self) -> str:
        return self.display_name or self.email

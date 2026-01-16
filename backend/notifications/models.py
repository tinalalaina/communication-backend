import uuid

from django.conf import settings
from django.db import models


class Notification(models.Model):
    TYPE_CHOICES = (
        ('friend_request', 'Demande d\'ami'),
        ('like', 'Like'),
        ('comment', 'Commentaire'),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    notif_type = models.CharField(max_length=30, choices=TYPE_CHOICES)
    message = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self) -> str:
        return f"Notification {self.notif_type} pour {self.user_id}"

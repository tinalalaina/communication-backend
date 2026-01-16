from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from notifications.models import Notification


def envoyer_notification(user, notif_type: str, message: str) -> Notification:
    notification = Notification.objects.create(
        user=user,
        notif_type=notif_type,
        message=message,
    )
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"user_{user.id}_notifications",
        {
            'type': 'notification.message',
            'id': str(notification.id),
            'notif_type': notif_type,
            'message': message,
            'created_at': notification.created_at.isoformat(),
            'is_read': notification.is_read,
        },
    )
    return notification

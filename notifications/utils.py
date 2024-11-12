from channels.db import database_sync_to_async
from .models import Notification
from .serializers import NotificationSerializer


@database_sync_to_async
def get_unread_notifications(user):
    notifications = Notification.objects.filter(
        user=user,
        is_read=False,
    )
    notification_serializer = NotificationSerializer(
        notifications,
        many=True,
    )
    return notification_serializer.data

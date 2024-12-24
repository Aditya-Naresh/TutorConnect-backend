from celery import shared_task
from .models import Notification
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .serializers import NotificationSerializer
from .utils import get_unread_notifications
from django.contrib.auth import get_user_model

User = get_user_model()


@shared_task
def send_notification_task(notification_id, user_id):
    channel_layer = get_channel_layer()
    try:
        notification = Notification.objects.get(id=notification_id)
        user = User.objects.get(id=user_id)

        serializer = NotificationSerializer(notification)
        notification_data = serializer.data
        group_name = f"notifications_{user.id}"

        async_to_sync(channel_layer.group_send)(
            group_name,
            {
                "type": "notification_message",
                "message": notification_data,
            },
        )

        unread_notifications = async_to_sync(get_unread_notifications)(user)
        async_to_sync(channel_layer.group_send)(
            group_name,
            {
                "type": "unread_notifications",
                "notifications": unread_notifications,
            },
        )
    except Exception as e:
        print(f"Error sending notification: {e}")

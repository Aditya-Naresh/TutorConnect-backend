from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Notification
from timeslots.models import TimeSlots
from django.contrib.auth import get_user_model
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .serializers import NotificationSerializer
from .utils import get_unread_notifications

User = get_user_model()


@receiver(post_save, sender=TimeSlots)
def send_timeslot_notification(sender, instance, **kwargs):
    if instance.status == TimeSlots.Status.BOOKED:
        print("Creating Booking Instance")
        notification_type = Notification.Types.BOOKING
        start_time = instance.start_time.strftime("%Y-%m-%d %H:%M")
        end_time = instance.end_time.strftime("%Y-%m-%d %H:%M")
        time = f"from {start_time} to {end_time}"
        message = f"{instance.tutor.first_name}'s time has been booked {time}."
        user_to_notify = instance.tutor
    elif instance.status == TimeSlots.Status.CANCELLED:
        print("Creating Cancellation Instance")
        notification_type = Notification.Types.CANCELLATION
        

        # Create notification
    notification = Notification.objects.create(
        user=user_to_notify,
        type=notification_type,
        message=message,
    )

    # Serialize notification data
    serializer = NotificationSerializer(notification)
    notification_data = serializer.data
    print("Serialized Data:", notification_data)
    # Send notification data through WebSocket
    channel_layer = get_channel_layer()
    group_name = f"notifications_{user_to_notify.id}"
    async_to_sync(channel_layer.group_send)(
        group_name,
        {
            "type": "notification_message",
            "message": notification_data,
        },
    )
    # Ensure unread notifications are retrieved synchronously
    unread_notifications = async_to_sync(
        get_unread_notifications,
    )(
        user_to_notify,
    )
    async_to_sync(channel_layer.group_send)(
        group_name,
        {
            "type": "unread_notifications",
            "notifications": unread_notifications,
        },
    )

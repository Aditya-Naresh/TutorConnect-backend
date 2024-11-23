from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Notification
from timeslots.models import TimeSlots
from django.contrib.auth import get_user_model
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .serializers import NotificationSerializer
from .utils import get_unread_notifications

User = get_user_model()

original_times = {}


@receiver(pre_save, sender=TimeSlots)
def cache_original_times(sender, instance, **kwargs):
    if instance.pk:
        try:
            original_instance = TimeSlots.objects.get(pk=instance.pk)
            original_times[instance.pk] = {
                "start_time": original_instance.start_time,
                "end_time": original_instance.end_time,
            }
        except TimeSlots.DoesNotExist:
            print("Time Slot does not exist")


@receiver(post_save, sender=TimeSlots)
def handle_time_slot_notifications(sender, instance, created, **kwargs):
    if not created:
        channel_layer = get_channel_layer()
        start_time = instance.start_time.strftime("%H:%M")
        end_time = instance.end_time.strftime("%H:%M")
        day = instance.start_time.strftime("%Y-%m-%d")
        time = f"session: from {start_time} to {end_time}"
        student = instance.student
        tutor = instance.tutor
        current_start = instance.start_time
        cached_times = original_times.pop(instance.pk, None)
        link = f"/timeslot-details/{instance.id}"
        if cached_times:
            original_start = cached_times["start_time"]
        if original_start != current_start:
            # Handle time updates or other status changes if needed
            print("TIME UPDATE")
            notification_type = Notification.Types.UPDATE
            message = f"Updated time of {time} on {day}."
            users_to_notify = [student]
        elif instance.status == TimeSlots.Status.BOOKED:
            notification_type = Notification.Types.BOOKING
            message = f"{instance.student.first_name} booked {time} on {day}."
            users_to_notify = [tutor]

        elif instance.status == TimeSlots.Status.CANCELLED:
            notification_type = Notification.Types.CANCELLATION
            cancelled_by = instance.cancelled_by
            cancelled_by_name = cancelled_by.get_full_name()
            message = f"{cancelled_by_name} cancelled {time} on {day}."
            # Notify the opposite party and all admins
            admins = list(User.objects.filter(role=User.Role.ADMIN))
            target_user = [tutor if cancelled_by == student else student]
            users_to_notify = target_user + admins
        elif instance.status == TimeSlots.Status.REFUNDED:
            notification_type = Notification.Types.ALERT
            message = "Money refunded for the cancelled Time Slot"
            users_to_notify = [student]
        # Create and send notifications to all relevant users
        notification_list = []
        for user in users_to_notify:
            notification = Notification.objects.create(
                user=user,
                type=notification_type,
                message=message,
                link=link,
            )
            notification_list.append(notification)
            print("notification: ", notification)

            # Send notification message through WebSocket
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

            # Send unread notifications count or data
            unread_notifications = async_to_sync(
                get_unread_notifications,
            )(user)
            async_to_sync(channel_layer.group_send)(
                group_name,
                {
                    "type": "unread_notifications",
                    "notifications": unread_notifications,
                },
            )

        print("Notification sent for:", notification_type)

from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Notification
from timeslots.models import TimeSlots
from django.contrib.auth import get_user_model
from .tasks import send_notification_task

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
            admins = list(User.objects.filter(role=User.Role.ADMIN))
            target_user = [tutor if cancelled_by == student else student]
            users_to_notify = target_user + admins
        elif instance.status == TimeSlots.Status.REFUNDED:
            notification_type = Notification.Types.ALERT
            message = "Money refunded for the cancelled Time Slot"
            users_to_notify = [student]
        else:
            return

        for user in users_to_notify:
            notification = Notification.objects.create(
                user=user,
                type=notification_type,
                message=message,
                link=link,
            )

            send_notification_task.delay(
                notification.id,
                user.id,
            )

from django.db.models.signals import post_save
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .consumers import AnalyticsConsumer
from timeslots.models import TimeSlots
from accounts.models import User


@receiver(post_save, sender=TimeSlots)
def refresh_analytics_on_timeslot_update(sender, instance, **kwargs):
    try:
        channel_layer = get_channel_layer()
        analytics_data = async_to_sync(AnalyticsConsumer.get_analytics_data)()

        async_to_sync(channel_layer.group_send)(
            "analytics_group",
            {
                "type": "send_analytics_update",
                "data": analytics_data,
            },
        )
    except Exception as e:
        print(
            f"Error refreshing analytics on Timeslot update: {str(e)}",
        )


@receiver(post_save, sender=User)
def refresh_analytics_on_user_creation(sender, instance, created, **kwargs):
    if created:
        try:
            channel_layer = get_channel_layer()
            analytics_data = async_to_sync(AnalyticsConsumer.get_analytics_data)()

            async_to_sync(channel_layer.group_send)(
                "analytics_group",
                {
                    "type": "send_analytics_update",
                    "data": analytics_data,
                },
            )
        except Exception as e:
            print(f"Error refreshing analytics on User creation: {str(e)}")

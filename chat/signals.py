from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Messages
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


@receiver(post_save, sender=Messages)
def handle_message_history(sender, instance, created, **kwargs):
    if created:
        channel_layer = get_channel_layer()
        chat_room = f"chat_{instance.chat_room.user1.id}_{instance.chat_room.user2.id}"
        print("message_history: ", instance)

        async_to_sync(channel_layer.group_send)(
            chat_room, {"type": "send_message_history"}
        )

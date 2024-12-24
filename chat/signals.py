from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Messages
from .tasks import send_message_history_task


@receiver(post_save, sender=Messages)
def handle_message_history(sender, instance, created, **kwargs):
    if created:
        try:
            user1id = instance.chat_room.user1.id
            user2id = instance.chat_room.user2.id
            chat_room = f"chat_{user1id}_{user2id}"
            send_message_history_task.delay(chat_room)
        except Exception as e:
            print(f"Error sending message history task: {e}")

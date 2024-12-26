from celery import shared_task
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


@shared_task
def send_message_history_task(chat_room):
    print(f"Sending message history for chat_room: {chat_room}")
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        chat_room,
        {
            "type": "send_message_histories",
        },
    )

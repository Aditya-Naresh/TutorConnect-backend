import types
import asyncio
from celery import shared_task
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from .consumers import AnalyticsConsumer

@shared_task
def broadcast_analytics_task():
    # Run the async function and await its result
    analytics_data = asyncio.run(AnalyticsConsumer.get_analytics_data())

    # Ensure that the data is serializable and not a coroutine
    if isinstance(analytics_data, types.CoroutineType):
        analytics_data = asyncio.run(analytics_data)

    channel_layer = get_channel_layer()

    # Since channel_layer.group_send is async, we use async_to_sync to call it synchronously
    async_to_sync(channel_layer.group_send)(
        "analytics_group",
        {
            "type": "send_analytics_update",
            "data": analytics_data,
        },
    )

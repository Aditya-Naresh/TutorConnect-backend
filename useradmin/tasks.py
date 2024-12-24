import types
import asyncio
from celery import shared_task
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from .consumers import AnalyticsConsumer


@shared_task
def broadcast_analytics_task():
    analytics_data = asyncio.run(AnalyticsConsumer.get_analytics_data())

    if isinstance(analytics_data, types.CoroutineType):
        analytics_data = asyncio.run(analytics_data)

    channel_layer = get_channel_layer()

    async_to_sync(channel_layer.group_send)(
        "analytics_group",
        {
            "type": "send_analytics_update",
            "data": analytics_data,
        },
    )

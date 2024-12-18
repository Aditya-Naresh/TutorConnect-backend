from django.urls import re_path
from .consumers import VideoCallConsumer, NotifyConsumer, BoardConsumer

websocket_urlpatterns = [
    re_path(
        r"ws/call/notification/(?P<id>\d+)/$",
        NotifyConsumer.as_asgi(),
    ),
    re_path(
        r"ws/video/call/(?P<userid>\d+)/$",
        VideoCallConsumer.as_asgi(),
    ),
    re_path(
        r"ws/whiteboard/(?P<timeSlot>\d+)/$",
        BoardConsumer.as_asgi(),
    ),
]

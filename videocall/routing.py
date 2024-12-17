from django.urls import re_path
from .consumers import VideoCallConsumer, NotifyConsumer

websocket_urlpatterns = [
    re_path(
        r"ws/call/notification/(?P<id>\d+)/$",
        NotifyConsumer.as_asgi(),
    ),
    re_path(
        r"ws/video/call/(?P<userid>\d+)/$",
        VideoCallConsumer.as_asgi(),
    ),
]

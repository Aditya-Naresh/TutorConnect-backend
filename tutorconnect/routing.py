from chat.routing import websocket_urlpatterns as chat_websocket_urlpatterns
from notifications.routing import (
    websocket_urlpatterns as notifications_websocket_urlpatterns,
)
from videocall.routing import (
    websocket_urlpatterns as videocall_websocket_urlpatterns,
)

websocket_urlpatterns = (
    chat_websocket_urlpatterns
    + notifications_websocket_urlpatterns
    + videocall_websocket_urlpatterns
)

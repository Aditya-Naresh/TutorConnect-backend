import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tutorconnect.settings")
django.setup()
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from .routing import websocket_urlpatterns
from .middlewares import JWTAuthMiddlewareStack

django_asgi_app = get_asgi_application()


application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        "websocket": JWTAuthMiddlewareStack(
            URLRouter(
                websocket_urlpatterns,
            )
        ),
    }
)

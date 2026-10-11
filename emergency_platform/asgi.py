import os

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "emergency_platform.settings")

django_asgi_app = get_asgi_application()

from incidents.routing import websocket_urlpatterns  # noqa: E402
from incidents.websocket_auth import WebSocketTokenMiddleware  # noqa: E402


application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AllowedHostsOriginValidator(
        WebSocketTokenMiddleware(URLRouter(websocket_urlpatterns))
    ),
})

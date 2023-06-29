from channels.auth import AuthMiddlewareStack
from channels.routing import URLRouter, ProtocolTypeRouter

from core import routing

application = ProtocolTypeRouter({
    'websocket':AuthMiddlewareStack(
        URLRouter(
            routing.websocket_urlpatterns
        )
    )
})
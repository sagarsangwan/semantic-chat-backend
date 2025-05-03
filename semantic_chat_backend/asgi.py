import os
from channels.routing import ProtocolTypeRouter
from django.core.asgi import get_asgi_application


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "semantic_chat_backend.settings")

django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        # "websocket": AllowedHostsOriginValidator(
        #     AuthMiddlewareStack(URLRouter(chat.routing.websocket_urlpatterns))
        # ),
    }
)

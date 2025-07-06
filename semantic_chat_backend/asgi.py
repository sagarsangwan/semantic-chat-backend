import os
from django.core.asgi import get_asgi_application
from socketio_server import socketio_app

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "semantic_chat_backend.settings")

django_asgi_app = get_asgi_application()
socketio_app.other_asgi_app = django_asgi_app  # merge DRF

application = socketio_app

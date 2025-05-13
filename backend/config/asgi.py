import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from comments.routing import websocket_urlpatterns

# Set default settings module for Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Define ASGI application with HTTP and WebSocket support
application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(websocket_urlpatterns)
    ),
})

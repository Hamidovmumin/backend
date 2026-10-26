from django.urls import path
from security.consumers import SecurityConsumer

websocket_urlpatterns = [
    path('ws/security/', SecurityConsumer.as_asgi()),
]

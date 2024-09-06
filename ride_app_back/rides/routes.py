from django.urls import path
from .consumers import RideConsumer

websocket_urlpatterns = [
    path("ws/rides/", RideConsumer.as_asgi()),
]
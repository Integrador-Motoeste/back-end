from django.urls import path
from .consumers import RideQueueConsumer

websocket_urlpatterns = [
    path("ws/rides_queue/<str:user_id>/<str:user_type>/", RideQueueConsumer.as_asgi()),
]
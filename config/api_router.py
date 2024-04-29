from django.conf import settings
from rest_framework.routers import DefaultRouter
from rest_framework.routers import SimpleRouter

from ride_app_back.motorcycles.api.viewsets import MotorcycleViewSet
from ride_app_back.ratings.api.viewsets import RatingViewSet
from ride_app_back.users.api.views import PilotViewSet
from ride_app_back.users.api.views import UserViewSet

router = DefaultRouter() if settings.DEBUG else SimpleRouter()

router.register("users", UserViewSet)
router.register("pilots", PilotViewSet)
router.register("ratings", RatingViewSet)
router.register("motorcycle", MotorcycleViewSet)

app_name = "api"
urlpatterns = router.urls

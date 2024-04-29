from django.conf import settings
from rest_framework.routers import DefaultRouter
from rest_framework.routers import SimpleRouter

from ride_app_back.users.api.views import UserViewSet, PilotViewSet
from ride_app_back.ratings.api.viewsets import RatingViewSet

router = DefaultRouter() if settings.DEBUG else SimpleRouter()

router.register("users", UserViewSet)
router.register("pilots", PilotViewSet)
router.register("ratings", RatingViewSet)

app_name = "api"
urlpatterns = router.urls

from django.conf import settings
from rest_framework.routers import DefaultRouter
from rest_framework.routers import SimpleRouter

from ride_app_back.motorcycles.api.viewsets import MotorcycleViewSet


router = DefaultRouter() if settings.DEBUG else SimpleRouter()



router.register("motorcycles", MotorcycleViewSet)

app_name = "motorcycles"
urlpatterns = router.urls


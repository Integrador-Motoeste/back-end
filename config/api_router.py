from django.conf import settings
from rest_framework.routers import DefaultRouter
from rest_framework.routers import SimpleRouter

from ride_app_back.motorcycles.api.viewsets import MotorcycleViewSet
from ride_app_back.notifications.api.views import NotificationViewSet
from ride_app_back.ratings.api.viewsets import RatingViewSet
from ride_app_back.rides.api.views import NearbyRidersViewSet
from ride_app_back.rides.api.views import RideViewSet
from ride_app_back.transactions.api.views import InvoiceViewSet
from ride_app_back.transactions.api.views import InvoicesAPIView, QRCodeView
from django.urls import path, include

from ride_app_back.users.api.views import UserViewSet


router = DefaultRouter() if settings.DEBUG else SimpleRouter()

router.register("ratings", RatingViewSet)
router.register("motorcycles", MotorcycleViewSet)
router.register("rides", RideViewSet)
router.register("invoices", InvoiceViewSet)
router.register("notifications", NotificationViewSet)
router.register("nearbyriders", NearbyRidersViewSet, basename="nearbyriders")
router.register("users", UserViewSet)

app_name = "api"
urlpatterns = router.urls + [
    path(
        "transactions/process_payment",
        InvoicesAPIView.as_view(),
        name="create_invoice",
    ),
    path(
        "transactions/get_qr_code",
        QRCodeView.as_view(),
        name="get_qr_code",
    )
] 


from django.conf import settings
from rest_framework.routers import DefaultRouter
from rest_framework.routers import SimpleRouter

from ride_app_back.motorcycles.api.viewsets import MotorcycleViewSet
from ride_app_back.notifications.api.views import NotificationViewSet
from ride_app_back.ratings.api.viewsets import RatingViewSet
from ride_app_back.rides.api.views import NearbyRidersViewSet
from ride_app_back.rides.api.views import RideViewSet
from ride_app_back.transactions.api.views import InvoiceViewSet
from ride_app_back.transactions.api.views import InvoicesAPIView, QRCodeView, PaymentWebHookview, WithdrawView
from django.urls import path, include

from ride_app_back.users.api.views import UserViewSet, TurnPilot

from django.conf import settings
from django.conf.urls.static import static

router = DefaultRouter() if settings.DEBUG else SimpleRouter()

router.register("ratings", RatingViewSet)
router.register("motorcycles", MotorcycleViewSet)
router.register("rides", RideViewSet)
router.register("invoices", InvoiceViewSet)
router.register("notifications", NotificationViewSet)
router.register("nearbyriders", NearbyRidersViewSet, basename="nearbyriders")
router.register("users", UserViewSet, basename="users")
router.register("turn_pilot", TurnPilot, basename="turn_pilot")  

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
    ),
    path(
        "transactions/payment_webhook",
        PaymentWebHookview.as_view(),
        name="payment_webhook",
    ),
    path(
        "transactions/withdraw",
        WithdrawView.as_view(),
        name="withdraw",
    ),
] 

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
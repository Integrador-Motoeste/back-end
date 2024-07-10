from django.urls import path

from ride_app_back.transactions.api.views import InvoicesAPIView

urlpatterns = [
    path(
        "create_invoice",
        InvoicesAPIView.as_view(),
        name="create_invoice",
    ),
]

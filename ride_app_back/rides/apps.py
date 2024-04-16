from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class RidesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "ride_app_back.rides"
    verbose_name = _("Corridas")

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class RatingsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "ride_app_back.ratings"
    verbose_name = _("Avaliações")

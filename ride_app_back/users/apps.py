import contextlib

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

class UsersConfig(AppConfig):
    name = "ride_app_back.users"
    verbose_name = _("Usuários")

    def ready(self):
        import ride_app_back.users.signals
        with contextlib.suppress(ImportError):
            import ride_app_back.users.signals  # noqa: F401
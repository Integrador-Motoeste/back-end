from django.conf import settings
from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext_lazy as _

from .forms import UserAdminChangeForm
from .forms import UserAdminCreationForm
from .models import User
from ..motorcycles.models import Motorcycle

if settings.DJANGO_ADMIN_FORCE_ALLAUTH:
    # Force the `admin` sign in process to go through the `django-allauth` workflow:
    # https://docs.allauth.org/en/latest/common/admin.html#admin
    admin.site.login = login_required(admin.site.login)  # type: ignore[method-assign]


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):
    # form = UserAdminChangeForm
    # add_form = UserAdminCreationForm
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Personal info"), {"fields": ("name", "email")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
        (_("Atributos do usuário"), {"fields": ("cpf", "birthday", "balance", "phone", "picture", "latitude", "longitude")}),
    )
    list_display = ["username", "name", "is_superuser"]
    search_fields = ["name"]

class MotocycleInline(admin.TabularInline):
    model = Motorcycle
    extra = 1

class PilotAdmin(admin.ModelAdmin):
    list_display = ["user", "cnh"]
    search_fields = ["user__name"]
    list_filter = ["user__name"]
    inlines = [MotocycleInline]


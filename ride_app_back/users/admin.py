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
        (_("Personal info"), {"fields": ("first_name", "email")}),
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
        (_("Atributos do usuário"), {"fields": ("cpf", "balance", "picture", "cnh", "status")}),
    )
    list_display = ["username", "first_name", "display_groups" ,"is_superuser"]
    search_fields = ["first_name"]

    def display_groups(self, obj):
        return ", ".join([group.name for group in obj.groups.all()])
    display_groups.short_description = 'Groups'

class MotocycleInline(admin.TabularInline):
    model = Motorcycle
    extra = 1

class PilotAdmin(admin.ModelAdmin):
    list_display = ["user", "cnh"]
    search_fields = ["user__name"]
    list_filter = ["user__name"]
    inlines = [MotocycleInline]


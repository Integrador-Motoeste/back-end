from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Avg
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django_cpf_cnpj.fields import CPFField

class PilotStatus(models.IntegerChoices):
    Inative = 0, _("Inativo")
    Active = 1, _("Ativo")
    Busy = 2, _("Ocupado")

class User(AbstractUser):
    """
    Default custom user model for ride-app-back.
    If adding fields that need to be filled at user signup,
    check forms.SignupForm and forms.SocialSignupForms accordingly.
    """

    class Meta:
        ordering = ["name"]
        verbose_name = "Usuário"
        verbose_name_plural = "Usuários"

    # First and last name do not cover name patterns around the globe
    name = models.CharField(_("Nome do Usuário"), blank=True, max_length=255)
    email = models.EmailField(_("email address"), unique=True)
    surname = models.CharField(_("Sobrenome"), blank=True, max_length=255)
    cpf = CPFField(verbose_name=_("CPF"))
    first_name = None  # type: ignore[assignment]
    last_name = None  # type: ignore[assignment]
    birthday = models.DateField(
        verbose_name=_("Data de Nascimento"),
        blank=True,
        null=True,
    )
    balance = models.DecimalField(
        verbose_name="Saldo",
        max_digits=100,
        decimal_places=2,
        default=0,
    )
    phone = models.CharField(verbose_name=_("Telefone"), max_length=15, unique=True)
    picture = models.ImageField(upload_to="uploads", verbose_name="Imagem")
    latitude = models.FloatField(verbose_name=(_("Latitude")), blank=True, null=True)
    longitude = models.FloatField(verbose_name=(_("Longitude")), blank=True, null=True)
    cnh = models.IntegerField(verbose_name="CNH", blank=True, null=True)
    status = models.IntegerField(
        choices=PilotStatus.choices, default=PilotStatus.Active, blank=True, null=True
    )

    @property
    def average_rating(self) -> float:
        return self.Ratings.objects.all().aggregate(Avg("rating"))["rating__avg"] or 0

    def get_absolute_url(self) -> str:
        """Get URL for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"username": self.username})

    def __str__(self) -> str:
        return self.username

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]


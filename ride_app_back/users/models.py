from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django_cpf_cnpj.fields import CPFField

from ..motorcycles.models import Motorcycle


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
    number = models.CharField(verbose_name=_("Telefone"), max_length=15)
    picture = models.ImageField(upload_to="uploads", verbose_name="Imagem")

    def get_absolute_url(self) -> str:
        """Get URL for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"username": self.username})


class Pilot:
    class Meta:
        ordering = ["user__name"]
        verbose_name = "Piloto"
        verbose_name_plural = "Pilotos"

    user = models.OneToOneField(
        User,
        verbose_name=_("Usuário"),
        related_name="user",
        on_delete=models.CASCADE,
    )
    motorcycle = models.ForeignKey(
        Motorcycle,
        verbose_name="Motos",
        related_name="motorcycles",
        on_delete=models.CASCADE,
    )
    cnh = models.IntegerField()
    status = models.IntegerField()

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
        ordering = ["first_name"]
        verbose_name = "Usuário"
        verbose_name_plural = "Usuários"

    id_clerk_user = models.CharField(max_length=255)
    email = models.EmailField(_("email address"), unique=True)
    first_name = models.CharField(_("Nome"), max_length=255)
    last_name = models.CharField(_("Sobrenome"), max_length=255)
    cpf = CPFField(verbose_name=_("CPF"))
    balance = models.DecimalField(
        verbose_name="Saldo",
        max_digits=100,
        decimal_places=2,
        default=0,
    )
    picture = models.ImageField(upload_to="uploads", verbose_name="Imagem")
    latitude = models.FloatField(verbose_name=(_("Latitude")), blank=True, null=True)
    longitude = models.FloatField(verbose_name=(_("Longitude")), blank=True, null=True)
    cnh = models.CharField(verbose_name="CNH", blank=True)
    status = models.IntegerField(
        choices=PilotStatus.choices, default=PilotStatus.Active, blank=True, null=True
    )
    username = models.CharField(max_length=255, unique=True, blank=True)

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

    def save(self, *args, **kwargs):
        if self.email and not self.username:
            self.username = self.email
        if self.username and not self.email:
            self.email = self.username
        super().save(*args, **kwargs)


    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "first_name", "last_name"]
    

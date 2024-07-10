from django.db import models
from django.utils.translation import gettext as _

from ..rides.models import Ride
from ..users.models import Pilot
from ..users.models import User

# Create your models here.
STATUS_GROUP_CHOICES = (
    ("pending", _("Aguardando pagamento")),
    ("completed", _("Pagamento concluído")),
)


class Transaction(models.Model):
    value = models.DecimalField(verbose_name="Valor", max_digits=20, decimal_places=2)
    time = models.DateTimeField(verbose_name="Data/Hora", auto_now=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_GROUP_CHOICES,
        null=False,
        verbose_name=_("Status"),
    )

    class Meta:
        verbose_name = "Transação"
        verbose_name_plural = "Transações"


class Invoice(models.Model):
    class Meta:
        verbose_name = "Fatura"
        verbose_name_plural = "Faturas"

    PAYMENT_METHODS_CHOICES = (
        ("PIX", _("Pix")),
        ("CREDIT_CARD", _("Cartão de crédito")),
    )

    PAYMENT_STATUS_CHOICES = (
        ("PENDING", _("Pendente")),
        ("RECEIVED", _("Recebido")),
        ("CONFIRMED", _("Confirmado")),
        ("CANCELED", _("Cancelado")),
    )

    external_id = models.CharField(
        max_length=50,
        editable=False,
        verbose_name=_("ID externo"),
        null=True,
        blank=True,
    )
    payment_type = models.CharField(
        max_length=50,
        choices=PAYMENT_METHODS_CHOICES,
        verbose_name=_("Tipo do pagamento"),
    )
    status = models.CharField(
        max_length=50,
        choices=PAYMENT_STATUS_CHOICES,
        default="PENDING",
        verbose_name=_("Status"),
    )
    link_payment = models.CharField(
        max_length=500,
        verbose_name=_("Link do pagamento"),
        null=True,
        blank=True,
    )
    transaction = models.OneToOneField(Transaction, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Usuário")
    ride = models.ForeignKey(Ride, on_delete=models.CASCADE, verbose_name="Corrida")
    pilot = models.ForeignKey(Pilot, on_delete=models.CASCADE, verbose_name="Piloto")

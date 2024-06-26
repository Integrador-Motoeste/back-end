from django.db import models
from simple_history.models import HistoricalRecords
from django.utils.translation import gettext_lazy as _
from ..users.models import User, Pilot

class Status(models.TextChoices):

    created = "created" , _("Criada")
    started = "started", _("Iniciada")
    finished = "finished", _("Finalizada")
    canceled = "canceled", _("Cancelada")

class Ride(models.Model):
    class Meta:
        ordering = ["timeStart"]
        verbose_name = _("Corrida")
        verbose_name_plural = _("Corridas")

    value = models.DecimalField(max_digits=6, decimal_places=2, 
        verbose_name="Valor"
        )
    distance = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name= _("Distância")
    )
    pilot = models.ForeignKey(
        Pilot,
        on_delete=models.PROTECT,
        verbose_name=_("Piloto"),
        null=True,
        related_name="pilot_rides"
    )
    client = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        verbose_name=_("Cliente"),
        related_name="rides"
    )
    start = models.CharField(max_length=100, verbose_name=_("Começo Local"))
    end = models.CharField(max_length=100, verbose_name=_("Chegada Local"))
    stopPlace = models.CharField(max_length=100, verbose_name=_("Local de Parada"), null=True, blank=True)
    status = models.CharField(choices=Status.choices, default=0, verbose_name=_("Status"))
    timeStart = models.DateTimeField(editable=False, auto_now_add=True, verbose_name=_("Início Tempo"),)
    timeEnd = models.DateTimeField(verbose_name=_("Fim Tempo"), null=True, blank=True)
    history = HistoricalRecords(verbose_name=_("Registro de Auditoria"))

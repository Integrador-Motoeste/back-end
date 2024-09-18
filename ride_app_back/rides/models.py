from django.db import models
from simple_history.models import HistoricalRecords
from django.utils.translation import gettext_lazy as _
from ..users.models import User

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

    distance = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name= _("Distância")
    )
    pilot = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        verbose_name=_("Piloto"),
        null=True,
        related_name="pilot_rides"
    )
    passenger = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        verbose_name=_("Passageiro"),
        related_name="rides"
    )

    start_lat = models.FloatField(verbose_name=_("Começo Latitude"))
    start_lng = models.FloatField(verbose_name=_("Começo Longitude"))
    end_lat = models.FloatField(verbose_name=_("Chegada Latitude"))
    end_lng = models.FloatField(verbose_name=_("Chegada Longitude"))

    origin = models.CharField(max_length=100, verbose_name=_("Origem"), null=True, blank=True)
    destination = models.CharField(max_length=100, verbose_name=_("Destino"), null=True, blank=True)

    stopPlace = models.CharField(max_length=100, verbose_name=_("Local de Parada"), null=True, blank=True)
    status = models.CharField(choices=Status.choices, default=0, verbose_name=_("Status"))
    timeStart = models.DateTimeField(editable=False, auto_now_add=True, verbose_name=_("Início Tempo"),)
    timeEnd = models.DateTimeField(verbose_name=_("Fim Tempo"), null=True, blank=True)
    duration = models.CharField(verbose_name=_("Duração Estimada"), null=True, blank=True)
    history = HistoricalRecords(verbose_name=_("Registro de Auditoria"))

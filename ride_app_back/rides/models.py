from django.db import models
from simple_history.models import HistoricalRecords

from ..users.models import User


# Create your models here.
class Ride(models.Model):
    class Meta:
        ordering = ["timeStart"]
        verbose_name = "Corrida"
        verbose_name_plural = "Corridas"

    value = models.DecimalField(max_digits=100, decimal_places=2, verbose_name="Valor")
    distance = models.DecimalField(
        max_digits=100,
        decimal_places=2,
        verbose_name="Distância",
    )
    pilot = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        verbose_name="Moto Taxi",
        null=True,
        related_name="pilot_rides",
    )
    client = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        verbose_name="Cliente",
        related_name="rides",
    )
    start = models.CharField(max_length=300, verbose_name="Começo")
    end = models.CharField(max_length=300, verbose_name="Chegada")
    status = models.BooleanField(default=True, verbose_name="Status")
    timeStart = models.DateTimeField(auto_now_add=True, verbose_name="Início")
    timeEnd = models.DateTimeField(verbose_name="Fim")
    history = HistoricalRecords(verbose_name="Registro de Auditoria")

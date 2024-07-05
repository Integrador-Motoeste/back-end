from django.db import models

from ..rides.models import Ride
from ..users.models import Pilot
from ..users.models import User

# Create your models here.


class Transaction(models.Model):
    value = models.DecimalField(verbose_name="Valor", max_digits=20, decimal_places=2)
    time = models.DateTimeField(verbose_name="Data/Hora", auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Usuário")
    pilot = models.ForeignKey(Pilot, on_delete=models.CASCADE, verbose_name="Piloto")
    ride = models.ForeignKey(Ride, on_delete=models.CASCADE, verbose_name="Corrida")

    class Meta:
        verbose_name = "Transação"
        verbose_name_plural = "Transações"

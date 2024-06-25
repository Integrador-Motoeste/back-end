from django.db import models

from ..users.models import Pilot

# Create your models here.


class Motorcycle(models.Model):
    class Meta:
        ordering = ["model"]
        verbose_name = "Moto"
        verbose_name_plural = "Motos"

    owner = models.ForeignKey(
        Pilot, verbose_name="Proprietário", on_delete=models.CASCADE, related_name="motorcycles"
    )
    model = models.CharField(max_length=100, verbose_name="Modelo")
    brand = models.CharField(max_length=100, verbose_name="Marca")
    color = models.CharField(max_length=100, verbose_name="Cor")
    year = models.IntegerField(verbose_name="Ano")
    plate = models.CharField(max_length=10, verbose_name="Placa")
    crlv = models.CharField(max_length=20)
    picture_moto = models.ImageField(upload_to="uploads", verbose_name="Imagem")

    def __str__(self) -> str:
        return self.model
from django.db import models

# Create your models here.


class Motorcycle(models.Model):
    class Meta:
        ordering = ["model"]
        verbose_name = "Moto"
        verbose_name_plural = "Motos"

    model = models.CharField(max_length=100, verbose_name="Modelo")
    brand = models.CharField(max_length=100, verbose_name="Marca")
    color = models.CharField(max_length=100, verbose_name="Cor")
    year = models.IntegerField(verbose_name="Ano")
    plate = models.CharField(max_length=10, verbose_name="Placa")
    crlv = models.CharField(max_length=20)
    picture_moto = models.ImageField(upload_to="uploads", verbose_name="Imagem")

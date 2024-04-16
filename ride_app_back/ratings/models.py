from django.db import models

from ..users.models import User

# Create your models here.


class Rating(models.Model):
    class Meta:
        ordering = ["title"]
        verbose_name = ["Avaliação"]
        verbose_name_plural = ["Avaliações"]

    title = models.CharField(max_length=50, verbose_name="Titulo")
    text = models.TextField(verbose_name="Comentário", blank=True, null=True)
    rating = models.IntegerField(verbose_name="Nota")
    owner = models.ForeignKey(
        User,
        verbose_name="Perfil",
        on_delete=models.CASCADE,
        related_name="ratings",
    )
    user = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        verbose_name="Cliente",
        related_name="rating",
    )

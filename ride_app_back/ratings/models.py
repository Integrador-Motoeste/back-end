from django.core.validators import MaxValueValidator
from django.core.validators import MinValueValidator
from django.db import models

from ..users.models import User

# Create your models here.


class Rating(models.Model):
    class Meta:
        ordering = ["title"]
        verbose_name = "Avaliação"
        verbose_name_plural = "Avaliações"

    title = models.CharField(max_length=50, verbose_name="Titulo")
    text = models.TextField(verbose_name="Comentário", blank=True, null=True)
    rating = models.DecimalField(
        verbose_name="Nota",
        decimal_places=2,
        max_digits=3,
        validators=[
            MaxValueValidator(5),
            MinValueValidator(1),
        ],
        default=1,
    )
    owner = models.ForeignKey(
        User,
        verbose_name="Dono",
        on_delete=models.CASCADE,
        related_name="OwnerRatings",
    )
    user = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        verbose_name="Destinatário",
        related_name="Ratings",
    )

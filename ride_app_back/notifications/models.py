from django.db import models

from ..users.models import User

# Create your models here.


class Notification(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="Destinatário"
    )
    message = models.TextField(verbose_name="Mensagem")
    status = models.BooleanField(default=False, verbose_name="Status")

    class Meta:
        verbose_name = "Notificação"
        verbose_name_plural = "Notificações"

from django.dispatch import receiver
from django.contrib.auth.models import Group
from django.db.models.signals import post_save
from .models import User


@receiver(post_save, sender=User)
def add_user_to_default_group(sender, instance, created, **kwargs):
    if created:
        print("User created")
        group, created = Group.objects.get_or_create(name='Passengers')
        instance.groups.add(group)
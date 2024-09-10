from django.dispatch import receiver
from django.contrib.auth.models import Group
from django.db.models.signals import post_save
from .models import User
import requests
from django.conf import settings
from .api.serializers import UserSerializer

CLERK_API_URL = 'https://api.clerk.dev/v1/users/'

@receiver(post_save, sender=User)
def sync_clerk_user(sender, instance, **kwargs):
    clerk_id = instance.id_clerk_user  # You need to store the Clerk user ID in your Django user model.
    user = UserSerializer(instance).data
    print("\n USERrrrrrrrrrrrrrrrrrrrrrrrrr: ", user)
    headers = {
        'Authorization': f'Bearer {settings.CLERK_API_KEY}',
        'Content-Type': 'application/json',
    }

    groups = list(instance.groups.values_list('name', flat=True))
    
    payload = {
        "publicMetadata": {
            "cpf": user.get("cpf"),
            "status": user.get("status"),
            "groups": groups,
            "cnh": user.get("cnh"),
            "balance": user.get("balance"),
            "latitude": user.get("latitude"),
            "longitude": user.get("longitude"),
        }
    }

    if instance.picture.url:
        payload["publicMetadata"]["image_url"] = user.get("picture")

    response = requests.patch(f'{CLERK_API_URL}{clerk_id}', json=payload, headers=headers)
    
    response.raise_for_status()
    print("\n RESPONSE: ", response.json())
    print(f'User {instance.username} synced with Clerk')


@receiver(post_save, sender=User)
def add_user_to_default_group(sender, instance, created, **kwargs):
    if created:
        print("User created")
        group, created = Group.objects.get_or_create(name='Passengers')
        instance.groups.add(group)
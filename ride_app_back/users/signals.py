from django.dispatch import receiver
from django.contrib.auth.models import Group
from django.db.models.signals import post_save, pre_save
from .models import User
import requests
from django.conf import settings
from .api.serializers import UserSerializer
import json
from rest_framework_simplejwt.tokens import RefreshToken

CLERK_API_URL = 'https://api.clerk.dev/v1/users/'

@receiver(post_save, sender=User)
def sync_clerk_user(sender, instance, created,**kwargs):
    user = UserSerializer(instance).data
    token = generate_access_token(instance)
    groups = list(instance.groups.values_list('name', flat=True))

    print(instance)

    if not instance.id_clerk_user and created:
        print("creating user clerk") 
        headers = {
            'Authorization': f'Bearer {settings.CLERK_API_KEY}',
            'Content-Type': 'application/json',
        }
        payload = {
            "first_name": instance.first_name,
            "last_name": instance.last_name,
            "email_address": [
                user.get("email")
            ],
            "password": '1234',
            "skip_password_checks": True,
            "skip_password_requirement": True,
            "public_metadata": {
                "cpf": user.get("cpf"),
                "status": instance.status,
                "groups": groups,
                "cnh": instance.cnh,
                "balance": instance.balance,
                "latitude": instance.latitude,
                "longitude": instance.longitude,
                "django_token": token,
            }
        }

        response = requests.post('https://api.clerk.com/v1/users', json=payload, headers=headers)

        if response.status_code != 201:
            print("Error creating user in Clerk:", response.status_code)
            print("Response body:", response.text)
            response.raise_for_status()

        instance.id_clerk_user = response.json().get('id')
        print(f'Clerk user created for {instance.username}')
        
    elif instance.id_clerk_user and not created:
        print('updating user clerk')
        clerk_id = instance.id_clerk_user  # You need to store the Clerk user ID in your Django user model.
        headers = {
            'Authorization': f'Bearer {settings.CLERK_API_KEY}',
            'Content-Type': 'application/json',
        }


        payload = {
            "public_metadata": {
                "cpf": user.get("cpf"),
                "status": user.get("status"),
                "groups": groups,
                "cnh": user.get("cnh"),
                "balance": user.get("balance"),
                "latitude": user.get("latitude"),
                "longitude": user.get("longitude"),
                "django_token": token,
            }
        }

        if instance.picture:
            payload["public_metadata"]["image_url"] = user.get("picture")

        response = requests.patch(f'{CLERK_API_URL}{clerk_id}', json=payload, headers=headers)

        response.raise_for_status()
        print("\n RESPONSE: ", response.json())
        print(f'User {instance.username} synced with Clerk')

        # Generate token for the user instance
        print("Generated Token:", token)

def generate_access_token(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

@receiver(post_save, sender=User)
def add_user_to_default_group(sender, instance, created, **kwargs):
    if created:
        print("User created")
        group, created = Group.objects.get_or_create(name='Passengers')
        instance.groups.add(group)

# @receiver(pre_save, sender=User)
# def create_clerk_user(sender, instance, **kwargs):
#     if not instance.id_clerk_user:
#         headers = {
#             'Authorization': f'Bearer {settings.CLERK_API_KEY}',
#             'Content-Type': 'application/json',
#         }
#         payload = {
#             "first_name": instance.first_name,
#             "last_name": instance.last_name,
#             "email_address": [
#                 instance.email
#             ],
#             "skip_password_checks": True,
#             "skip_password_requirement": True,
#         }
#         print('PAYLOAD:', payload)

#         response = requests.post('https://api.clerk.dev/v1/users', json=payload, headers=headers)

#         if response.status_code != 201:  
#             print("Erro ao criar usuário no Clerk:", response.status_code, response.json()) 
#             response.raise_for_status()

#         instance.id_clerk_user = response.json().get('id')
#         print(f'Clerk user created for {instance.username}')
    
#     print("INSTANCE:", instance)
# adminteste@gmail.com
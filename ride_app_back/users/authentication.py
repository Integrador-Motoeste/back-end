import requests
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.conf import settings
from django.contrib.auth.models import User

class ClerkAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return None

        try:
            token_type, token = auth_header.split(' ')
            if token_type.lower() != 'bearer':
                raise AuthenticationFailed('Invalid token type')
        except ValueError:
            raise AuthenticationFailed('Invalid token format')

        # Valida o token com o Clerk
        url = "https://api.clerk.dev/v1/tokens/verify"
        headers = {
            'Authorization': f'Bearer {settings.CLERK_API_KEY}',
            'Content-Type': 'application/json'
        }
        data = {
            'token': token
        }
        response = requests.post(url, json=data, headers=headers)
        print(response.json())

        if response.status_code != 200:
            raise AuthenticationFailed('Invalid token')

        clerk_user_id = response.json().get('sub')
        if not clerk_user_id:
            raise AuthenticationFailed('Invalid token payload')

        # Obtenha ou crie o usuário Django correspondente
        user, created = User.objects.get_or_create(id_clerk_user=clerk_user_id)
        return (user, None)
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import AccessToken

from django.views.decorators.csrf import csrf_exempt

from ride_app_back.users.models import User

from .serializers import UserSerializer

from django.contrib.auth.models import Group

from django.conf import settings

import requests

class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = []

    @action(detail=False)
    def me(self, request):
        serializer = UserSerializer(request.user, context={"request": request})
        return Response(status=status.HTTP_200_OK, data=serializer.data)
    
    @action(detail=False, methods=['get'])
    def turn_user_pilot(self, request):
        user = request.user
        user.groups.remove(1)
        group, created = Group.objects.get_or_create(name='Pilots')
        user.groups.add(group)
        user.save()
        return Response(status=status.HTTP_200_OK)
    
    @csrf_exempt
    @action(detail=False, methods=['post'])
    def create_user(self, request):
        email = request.data.get('email')
        first_name = request.data.get('first_name')
        last_name = request.data.get("last_name")
        id_clerk_user = request.data.get("id_clerk_user")
        
        if request.data.get("password"):
            password = request.data.get("password")
            user = User.objects.create_user(email=email, password=password, first_name=first_name, last_name=last_name, id_clerk_user=id_clerk_user)
            created = True
        
        else:
            try:
                user = User.objects.get(email=email)
                user.first_name = first_name
                user.last_name = last_name
                user.id_clerk_user = id_clerk_user
                user.save()
                created = False

            except User.DoesNotExist:
                user = User.objects.create(email=email, first_name=first_name, last_name=last_name, id_clerk_user=id_clerk_user)
                created = True

        print("\nUser created or updated", user)

        serializer = UserSerializer(user)
        return Response(status=status.HTTP_200_OK, data=serializer.data)
    
    def load_data_user_in_clerk(self, user):
        url = "https://api.clerk.dev/v1/users"
        headers = {
            'Authorization': f'Bearer {settings.CLERK_API_KEY}',
            'Content-Type': 'application/json'
        }

        data = {
            'cpf': user.cpf,
            'cnh': user.cnh,
            'status': user.status,
            'balance': user.balance,
            'imageUri': user.picture,
        }

        response = requests.post(url, json=data, headers=headers)


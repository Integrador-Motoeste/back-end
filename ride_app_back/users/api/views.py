from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from django.views.decorators.csrf import csrf_exempt
from drf_spectacular.utils import extend_schema
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.exceptions import ParseError

from ride_app_back.users.models import User

from .serializers import UserSerializer, TurnUserPilotSerializer, PilotSerializer
from ride_app_back.motorcycles.api.serializers import MotorcycleSerializer

from django.contrib.auth.models import Group
from rest_framework import serializers
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView



class GoogleLogin(SocialLoginView): 
    adapter_class = GoogleOAuth2Adapter
    callback_url = "http://localhost:8081/"
    client_class = OAuth2Client

class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = []


    @action(detail=False)
    def me(self, request):
        serializer = UserSerializer(request.user, context={"request": request})
        return Response(status=status.HTTP_200_OK, data=serializer.data)


    @action(detail=False, methods=['get'])
    def get_pilot_info(self, request):
        id = request.query_params.get('id')
        if not id:
            return Response({"error": "id parameter is required"}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.get(id=id)
        if not user:
            return Response({"error": "User not found"}, status=status.HTTP_204_NO_CONTENT)
        
        user_data = self.get_serializer(user).data
        motorcycle = user.motorcycles.all().first()
        motorcycle_data = MotorcycleSerializer(motorcycle).data


        response = {
            "user": user_data,
            "motorcycle": motorcycle_data
        }

        return Response(response, status=status.HTTP_200_OK)

class TurnPilot(GenericViewSet):
    serializer_class = TurnUserPilotSerializer

    @action(detail=False, methods=['post'])
    def post(self, request):
        # Verifica se o usuário já é um piloto
        if request.user.groups.filter(name='Pilots').exists():
            return Response({"error": "User is already a pilot"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Valida os dados do serializer
        serializer = TurnUserPilotSerializer(data=request.data)
        if not serializer.is_valid():
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        
        pilot_data = PilotSerializer(serializer.validated_data.get('pilot'))
        motorcycle_data = MotorcycleSerializer(serializer.validated_data.get('motorcycle'))
        
        if pilot_data.is_valid() and motorcycle_data.is_valid():
    
            # Atualiza os atributos do piloto
            pilot = request.user
            for attr, value in pilot_data.items():
                setattr(pilot, attr, value)
            
            # Altera o grupo do piloto
            pilot.groups.remove(Group.objects.get(id=1))  # Remove do grupo antigo
            pilot.groups.add(Group.objects.get(id=2))  # Adiciona ao grupo dos pilotos
    
            # Salva o usuário atualizado
            pilot.save()
    
            # Verifica e valida os dados da moto
            if motorcycle_data is None:
                return Response({"error": "Motorcycle data is required"}, status=status.HTTP_400_BAD_REQUEST)
    
            motorcycle_serializer = MotorcycleSerializer(data=motorcycle_data)
            if motorcycle_serializer.is_valid():
                motorcycle = motorcycle_serializer.save()
            else:
                return Response(motorcycle_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Retorna os dados atualizados do piloto e da moto
        return Response({
            "pilot": PilotSerializer(pilot).data,
            "motorcycle": MotorcycleSerializer(motorcycle).data
        }, status=status.HTTP_200_OK)

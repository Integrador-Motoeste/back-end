from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from django.views.decorators.csrf import csrf_exempt
from ride_app_back.motorcycles.api.serializers import MotorcycleSerializer

from ride_app_back.users.models import User

from .serializers import UserSerializer
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

    @action(detail=False, methods=['post'])
    def turn_user_pilot(self, request):
        user_serializer = self.get_serializer(request.data['user'])
        motorcycle_serializer = MotorcycleSerializer(data=request.data['motorcycle'])

        if user_serializer.is_valid() and motorcycle_serializer.is_valid():
            user = request.user
            user.groups.remove(1)
            group, created = Group.objects.get_or_create(name='Pilots')
            user.groups.add(group)
            user.cpf = user_serializer.validated_data['cpf']
            user.cnh = user_serializer.validated_data['cnh']
            user.save()

            if motorcycle_serializer.is_valid():
                motorcycle = motorcycle_serializer.save(owner=user)
                return Response({
                    "user": UserSerializer(user).data,
                    "motorcycle": MotorcycleSerializer(motorcycle).data
                }, status=status.HTTP_200_OK)
            else:
                return Response(motorcycle_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

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

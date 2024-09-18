from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from django.views.decorators.csrf import csrf_exempt
from ride_app_back.motorcycles.api.serializers import MotorcycleSerializer

from ride_app_back.users.models import User

from .serializers import UserSerializer

from django.contrib.auth.models import Group

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
    def create_or_update_user(self, request):
        email = request.data.get('email')
        first_name = request.data.get('first_name')
        last_name = request.data.get("last_name")

        user, created = User.objects.get_or_create(email=email, first_name=first_name, last_name=last_name)

        if not created:
            print("User already exists")
            user.first_name = first_name
            user.last_name = last_name
            user.save()
            
        print("usuario criado",user)
        serializer = UserSerializer(user)
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

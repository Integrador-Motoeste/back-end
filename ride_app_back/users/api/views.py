from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from django.views.decorators.csrf import csrf_exempt

from ride_app_back.users.models import User

from .serializers import UserSerializer, TurnUserPilotSerializer

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
        serializer_class = TurnUserPilotSerializer
        user = request.user
        user.groups.remove(1)
        group, created = Group.objects.get_or_create(name='Pilots')
        user.groups.add(group)
        user.save()
        return Response(status=status.HTTP_200_OK)

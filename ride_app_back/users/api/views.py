from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from ride_app_back.users.models import Pilot
from ride_app_back.users.models import User

from .serializers import PilotSerializer
from .serializers import UserSerializer


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=False)
    def me(self, request):
        serializer = UserSerializer(request.user, context={"request": request})
        return Response(status=status.HTTP_200_OK, data=serializer.data)


class PilotViewSet(ModelViewSet):
    queryset = Pilot.objects.all()
    serializer_class = PilotSerializer

    def get_queryset(self, *args, **kwargs):
        return self.queryset.filter(user=self.request.user)

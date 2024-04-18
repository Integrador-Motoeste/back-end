from rest_framework import status
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from .serializers import UserSerializer, PilotSerializer
from ride_app_back.users.models import User, Pilot

class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = "username"

    def get_queryset(self, *args, **kwargs):
        return self.queryset.filter(id=self.request.user.id)

    @action(detail=False)
    def me(self, request):
        serializer = UserSerializer(request.user, context={"request": request})
        return Response(status=status.HTTP_200_OK, data=serializer.data)


class PilotViewSet(ModelViewSet):
    queryset = Pilot.objects.all()
    serializer_class = PilotSerializer

    def get_queryset(self, *args, **kwargs):
        return self.queryset.filter(user=self.request.user)
    
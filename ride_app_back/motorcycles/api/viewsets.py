from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from ..models import Motorcycle
from .serializers import MotorcycleSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, CreateModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework import status


class MotorcycleViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Motorcycle.objects.all()
    serializer_class = MotorcycleSerializer

    @action(detail=False, methods=['get'])
    def my_motorcycle(self, request): 
        vehicles = Motorcycle.objects.filter(owner=request.user).first()
        serializer = self.get_serializer(vehicles)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def delete(self, request):
        vehicles = Motorcycle.objects.filter(owner=request.user).first()
        if vehicles:
            vehicles.delete()
        return Response(status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['post'])
    def create_motorcycle(self, request):
        serializer = MotorcycleSerializer(data=request.data)

        if request.user.groups.filter(name='Pilots').exists():
            if serializer.is_valid():
                serializer.save(owner=request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "Usuário não autorizado"}, status=status.HTTP_401_UNAUTHORIZED)

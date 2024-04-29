from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from ..models import Motorcycle
from .serializers import MotorcycleSerializer


class MotorcycleViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Motorcycle.objects.all()
    serializer_class = MotorcycleSerializer

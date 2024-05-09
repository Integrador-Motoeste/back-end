from rest_framework import status
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.response import Response
from .serializers import RideSerializer
from ..models import Ride
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, CreateModelMixin

class RideViewSet(ListModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, CreateModelMixin, GenericViewSet):
    queryset = Ride.objects.all()
    serializer_class = RideSerializer

    @action(detail=True, methods=['get'])
    def start(self, request, pk=None):
        ride = self.get_object()
        ride.status = 1
        ride.save()
        return Response(status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['get'])
    def finish(self, request, pk=None):
        ride = self.get_object()
        ride.status = 2
        ride.save()
        return Response(status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['get'])
    def cancel(self, request, pk=None):
        ride = self.get_object()
        ride.status = 3
        ride.save()
        return Response(status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['get'])
    def my_rides(self, request):
        rides = Ride.objects.filter(client=request.user)
        serializer = self.get_serializer(rides, many=True)
        return Response(serializer.data)
    

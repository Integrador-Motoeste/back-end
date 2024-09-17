from rest_framework import status
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.response import Response
from .serializers import RideSerializer
from ..models import Ride
from geopy.distance import geodesic
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, CreateModelMixin
from rest_framework.permissions import IsAuthenticated
from ...users.models import User
from ...users.api.serializers import UserSerializer

class RideViewSet(RetrieveModelMixin, CreateModelMixin, GenericViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Ride.objects.all()
    serializer_class = RideSerializer

    def create(self, request, *args, **kwargs):
        if request.user.groups.filter(name='Pilots').exists():
            if request.user.pilot_rides.filter(status=1).exists():
                return Response({"error": "Você já está em uma corrida"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            if request.user.rides.filter(status=1).exists():
                return Response({"error": "Você já está em uma corrida"}, status=status.HTTP_400_BAD_REQUEST)
        
        return super().create(request, *args, **kwargs)

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
    
    @action(detail=False, methods=['get'])
    def get_active_ride(self, request):
        rides = Ride.objects.filter(client=request.user, status=1).first()
        serializer = self.get_serializer(rides)
        return Response(serializer.data)

    
class NearbyRidersViewSet(GenericViewSet):
    queryset = User.objects.all()

    def list(self, request):
        user = request.user
        latitude = user.latitude
        longitude = user.longitude
        point = (latitude, longitude)

        nearby_riders = []
        for pilot in User.objects.filter(status = 1, groups__name = 'Pilots'):
            pilot_point = (pilot.latitude, pilot.longitude)
            distance = geodesic(point, pilot_point).km
            if distance <= 5:
                nearby_riders.append(pilot)
        
        serializer = UserSerializer(nearby_riders, many=True)
        return Response(serializer.data)
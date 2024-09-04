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

class RideViewSet(ListModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, CreateModelMixin, GenericViewSet):
    permission_classes = [IsAuthenticated]
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
    
class NearbyRidersViewSet(GenericViewSet):
    queryset = User.objects.all()

    def list(self, request):
        user = request.user
        latitude = user.latitude
        longitude = user.longitude
        point = (latitude, longitude)

        nearby_riders = []
        for pilot in User.objects.filter(status = 1):
            pilot_point = (pilot.latitude, pilot.longitude)
            distance = geodesic(point, pilot_point).km
            if distance <= 5:
                nearby_riders.append(pilot)
        
        serializer = UserSerializer(nearby_riders, many=True)
        return Response(serializer.data)
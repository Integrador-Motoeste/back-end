from rest_framework import serializers
from ..models import Ride

class RideSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ride
        fields = ['value', 'distance', 'pilot', 'client', 'start', 'end', 'stopPlace', 'status', 'timeStart', 'timeEnd']

        

    
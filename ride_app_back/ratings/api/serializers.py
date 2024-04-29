from rest_framework import serializers
from ride_app_back.ratings.models import Rating

class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ['id','title','text','rating','owner','user']
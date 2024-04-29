from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from .serializers import RatingSerializer
from ride_app_back.ratings.models import Rating

class RatingViewSet(ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
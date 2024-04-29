from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from ride_app_back.ratings.models import Rating

from .serializers import RatingSerializer


class RatingViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer

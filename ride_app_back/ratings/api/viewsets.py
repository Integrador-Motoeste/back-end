from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from ride_app_back.ratings.models import Rating
from .serializers import RatingSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Avg

class RatingViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer

    @action(detail=True, methods=['get'], url_path='average-rating')
    def average_rating(self, request, pk=None):
   
        ratings = Rating.objects.filter(user_id=pk)
        average = ratings.aggregate(average_rating=Avg('rating'))['average_rating'] or 0
        return Response({'average_rating': average})
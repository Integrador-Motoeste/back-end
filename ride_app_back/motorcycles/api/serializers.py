from rest_framework import serializers

from ..models import Motorcycle


class MotorcycleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Motorcycle
        fields = [
            "owner",
            "model",
            "brand",
            "color",
            "year",
            "plate",
            "crlv",
            "picture_moto",
        ]

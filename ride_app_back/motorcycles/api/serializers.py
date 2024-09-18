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


    picture_moto = serializers.SerializerMethodField()


    def get_picture_moto(self, obj):
        if obj.picture_moto:
            return obj.picture_moto.url
        return None
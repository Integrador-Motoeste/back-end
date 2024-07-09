from rest_framework import serializers

from ..models import Transaction


class TransactionSerializer(serializers.Serializer):
    class Meta:
        model = Transaction
        fields = [
            "value",
            "time",
            "user",
            "pilot",
            "ride",
        ]

from rest_framework import serializers

from ..models import Invoice
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


class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = [
            "external_id",
            "payment_type",
            "status",
            "link_payment",
            "transaction",
        ]

    external_id = serializers.CharField(read_only=True)
    link_payment = serializers.CharField(read_only=True)


class CreateInvoiceSerializer(serializers.Serializer):
    id = serializers.IntegerField()

    def validate_invoice_id(self, value):
        try:
            invoice = Invoice.objects.get(id=value)
        except Invoice.DoesNotExist:
            raise serializers.ValidationError("Pagamento não encontrado.")
        return invoice


class CPFField(serializers.Field):
    def to_representation(self, value):
        return str(value)


class AsaasCustomerSerializer(serializers.Serializer):
    externalReference = serializers.CharField(source="id")
    name = serializers.SerializerMethodField()
    cpfCnpj = CPFField(source="cpf")
    email = serializers.EmailField()

    def get_name(self, obj):
        return obj.get_full_name()

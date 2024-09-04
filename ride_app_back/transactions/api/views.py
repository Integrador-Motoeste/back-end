from datetime import datetime
from datetime import timedelta

from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from ride_app_back.transactions.models import Invoice

from ..asaas import AssasPaymentClient
from .serializers import CreateInvoiceSerializer
from .serializers import InvoiceSerializer


class InvoiceViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer



class InvoicesAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(request=CreateInvoiceSerializer)
    def post(self, request):
        serializer = CreateInvoiceSerializer(data=request.data)
        if serializer.is_valid():
            invoice_id = serializer.validated_data["id"]
            invoice = Invoice.objects.get(id=invoice_id)

            client = AssasPaymentClient()
            customer = client.create_or_update_customer(invoice.user)
            data = self.prepare_payment_data(invoice, customer)
            response = self.send_payment_request(data)

            if response:
                self.update_invoice(invoice, response)
                return Response(response, status=status.HTTP_200_OK)
            else:
                return Response(
                    {"error": "Erro ao enviar solicitação de pagamento"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def prepare_payment_data(self, invoice, customer):
        end_date = datetime.now() + timedelta(days=1)
        end_date_str = end_date.strftime("%Y-%m-%d")
        data = {
            "customer": customer.get("id"),
            "billingType": invoice.payment_type,
            "value": float(invoice.value),
            "dueDate": end_date_str,
            "description": "Chame seu mototaxi da maneira mais rápida!",
            "externalReference": str(invoice.id),
            "cpfCnpj": str(invoice.user.cpf),
        }
        return data

    def send_payment_request(self, data):
        client = AssasPaymentClient()
        response = client.send_payment_request(data)
        return response

    def update_invoice(self, invoice, result):
        invoice.link_payment = result.get("invoiceUrl", "")
        invoice.external_id = result.get("id", "")
        invoice.save()


class QRCodeView(APIView):

    @extend_schema(request=CreateInvoiceSerializer)
    def post(self, request):
        serializer = CreateInvoiceSerializer(data=request.data)
        if serializer.is_valid():
            invoice_id = serializer.validated_data["id"]
            invoice = Invoice.objects.get(id=invoice_id)

            client = AssasPaymentClient()
            response = client.get_qr_code(invoice.external_id)

            if response:
                return Response(response, status=status.HTTP_200_OK)
            else:
                return Response(
                    {"error": "Erro ao gerar QR Code"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

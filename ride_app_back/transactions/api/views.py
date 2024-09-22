from datetime import datetime
from datetime import timedelta
import json
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from ride_app_back.transactions.models import Invoice

from ..asaas import AssasPaymentClient
from .serializers import CreateInvoiceSerializer, WithDrawSerializer
from .serializers import InvoiceSerializer
from django.db.models import Q
from ride_app_back.users.models import User

class InvoiceViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer

    @action(detail=False, methods=['get'])
    def get_invoice_by_ride_id(self, request):
        id = request.query_params.get('id')

        if not id:
            return Response({"error": "id parameter is required"}, status=status.HTTP_400_BAD_REQUEST)
        invoice = Invoice.objects.filter(
            ride=id,
        ).first()

        serializer = self.get_serializer(invoice)
        if invoice:
            return Response(serializer.data)
        
        return Response({"error": "Corrida não encontrada"}, status=status.HTTP_400_BAD_REQUEST)



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



class WithdrawView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(request=WithDrawSerializer)
    def post(self, request):
        serializer = WithDrawSerializer(data=request.data)
        if serializer.is_valid():
            value = serializer.validated_data["value"]
            pilot = User.objects.get(id=request.user.id)

            if pilot.groups.filter(name="pilot").exists() == False:
                return Response(
                    {"error": "Usuário não é um piloto"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            if pilot.balance < value:
                return Response(
                    {"error": "Saldo insuficiente para saque"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            
            data = self.prepare_payment_data(pilot, value)
            response = self.send_payment_request(data)

            if response:
                pilot.balance = float(pilot.balance) - value
                pilot.save()
                return Response(response, status=status.HTTP_200_OK)


        return Response(
            {"error": "Erro ao enviar solicitação de pagamento"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    def prepare_payment_data(self, pilot, value):
        data = {
            "value" : value,
            "pixAddressKey" : str(pilot.cpf),
            "pixAddressKeyType" : "CPF",
            "scheduleDate": None,
            "description": "Pagamento de corrida",
        }
        return data

    def send_payment_request(self, data):
        client = AssasPaymentClient()
        response = client.send_withdraw_request(data)
        return response


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
    

#Only work with public IP
class PaymentWebHookview(APIView):

    def post(self, request):
        data = json.loads(request.body)
        print(data)
        if data:
            return Response(status=status.HTTP_200_OK)
        
        return Response(status=status.HTTP_400_BAD_REQUEST)

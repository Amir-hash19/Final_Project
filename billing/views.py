from rest_framework.generics import CreateAPIView, ListAPIView
from .models import Invoice, Payment, Transaction
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from account.permissions import GroupPermission
from .serializers import InvoiceSerializer, UserListSerializer, PaymentSerializer
from account.models import CustomUser
from django.db import models
from django.db import transaction


class CreateInvoiceView(CreateAPIView):
    queryset = Invoice.objects.all()
    permission_classes = [IsAuthenticated, GroupPermission("supportPanel", "SuperUser")]
    serializer_class = InvoiceSerializer







class UserWithoutInvoiceView(ListAPIView):
    serializer_class = UserListSerializer
    permission_classes = [IsAuthenticated, GroupPermission("supportPanel", "SuperUser")]

    def get_queryset(self):
        return CustomUser.objects.filter(invoice_set__isnull=True)
        





class CreatePaymentView(CreateAPIView):
    queryset = Payment.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = PaymentSerializer



    def perform_create(self, serializer):
        with transaction.atomic():
            payment = serializer.save(user = self.request.user)

            total_paid = Payment.objects.filter(
                invoice=payment.invoice,
                is_verified=True
            ).aggregate(total=models.Sum('amount'))['total'] or 0

            
            total_paid += payment.amount

            if total_paid >= payment.invoice.amount:
                payment.invoice.is_paid = True
                payment.invoice.save()
        

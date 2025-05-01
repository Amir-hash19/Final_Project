from rest_framework.generics import CreateAPIView, ListAPIView
from .models import Invoice, Payment, Transaction
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from account.permissions import GroupPermission
from .serializers import InvoiceSerializer, UserListSerializer, PaymentSerializer, PaymentListSerializer
from account.models import CustomUser
from django.db import models
from django.db import transaction
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend



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
        
        payment = serializer.save(user=self.request.user)

        total_paid = Payment.objects.filter(
            invoice=payment.invoice,
            is_verified=True
        ).aggregate(total=models.Sum('amount'))['total'] or 0

       
        if payment.is_verified:
            total_paid += payment.amount

        if total_paid >= payment.invoice.amount:
            payment.invoice.is_paid = True
            payment.invoice.save()






class ListPaymentAdminsView(ListAPIView):
    queryset = Payment.objects.all()
    permission_classes = [IsAuthenticated, GroupPermission("SupportPanel", "SuperUser")]
    serializer_class = PaymentListSerializer
    search_fields = ["is_verified", "paid_at", "user"]
    filterset_fields = ["is_verified", "method"]
    ordering_fields = ["-paid_at"]



class ListPaymentUserView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ["is_verified", "paid_at"]
    filterset_fields = ["is_verified", "method"]
    ordering_fields = ["-paid_at"]

    def get_queryset(self):
        return Payment.objects.filter(user=self.request.user)





class GetTransactionAdminView(ListAPIView):
    queryset = Transaction.objects.all()
    permission_classes = [IsAuthenticated, GroupPermission("SupportPanel", "SuperUser")]
    serializer_class = PaymentListSerializer
    search_fields = ["is_verified", "paid_at", "user"]
    filterset_fields = ["is_verified", "method"]
    ordering_fields = ["-paid_at"]
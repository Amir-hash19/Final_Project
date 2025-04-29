from rest_framework.generics import CreateAPIView
from .models import Invoice, Payment, Transaction
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from account.permissions import GroupPermission



class CreateInvoiceView(CreateAPIView):
    queryset = Invoice.objects.all()
    permission_classes = [IsAuthenticated, GroupPermission("supportPanel", "SuperUser")]
    serializer_class = InvoiceSerializer
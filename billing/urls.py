from django.urls import path
from .views import CreateInvoiceView, UserWithoutInvoiceView, CreatePaymentView, ListPaymentAdminsView, ListPaymentUserView, GetTransactionAdminView



urlpatterns = [
    path("create-invoice/", CreateInvoiceView.as_view(), name="create-invoice"),
    path("user-null-invoice/", UserWithoutInvoiceView.as_view(), name="no-invoices-list"),
    path("create-payment-user/", CreatePaymentView.as_view(), name="create-payment-user"),
    path("payment-list-admin/", ListPaymentAdminsView.as_view(), name="payment-list-admin"),
    path("list-payment-user/", ListPaymentUserView.as_view(), name="list-payment-user"),
    path("list-transaction-admin/", GetTransactionAdminView.as_view(), name="list-transaction-admin"),


]

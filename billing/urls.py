from django.urls import path
from .views import CreateInvoiceView, UserWithoutInvoiceView



urlpatterns = [
    path("create-invoice/", CreateInvoiceView.as_view(), name="create-invoice"),
    path("user-null-invoice/", UserWithoutInvoiceView.as_view(), name="no-invoices-list"),

]

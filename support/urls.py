from django.urls import path
from .views import CreateTicketView



urlpatterns = [
    path("create-ticket/", CreateTicketView.as_view(), name="add-ticket-by-user"),
]

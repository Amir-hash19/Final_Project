from django.urls import path
from .views import CreateTicketView, CreateMessageTicketView, ListTicketView, CreateMessageByAdminView



urlpatterns = [
    path("create-ticket/", CreateTicketView.as_view(), name="add-ticket-by-user"),
    path("ticket-list/", ListTicketView.as_view(), name="ticket-list"),
    path("create-message-admin/", CreateMessageByAdminView.as_view(), name="create-message-admin"),
    path("ticket/<int:ticket_id>/message/", CreateMessageTicketView.as_view(), name="add-messageticket-by-user"),

]

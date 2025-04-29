from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Ticket, TicketMessage
from account.permissions import GroupPermission
from .serializers import TicketSerializer, TicketMessageSerializer
from django.shortcuts import get_object_or_404
from account.views import CustomPagination
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend




class CreateTicketView(CreateAPIView):#کاربر عادی میتونه تیکت بزنه و صاحب تیکت خودشه
    permission_classes = [IsAuthenticated]
    serializer_class = TicketSerializer


    def perform_create(self, serializer):
        serializer.save(
            user=self.request.user
        )
                  



class CreateMessageTicketView(CreateAPIView):#ساختن پیام تیکت برای تیکت مورد نظر کاربر جاری
    permission_classes = [IsAuthenticated]
    serializer_class = TicketMessageSerializer

    def perform_create(self, serializer):
        ticket_id = self.request.data.get('ticket_id')
        ticket = get_object_or_404(Ticket, id=ticket_id) 
        serializer.save(
            sender=self.request.user,
            ticket=ticket
        )
        


class ListTicketView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TicketSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ["title", "created_at", "description"]
    filterset_fields = ["created_at", "status"]
    ordering_fields = ["-created-at"]

    def get_queryset(self):
        return Ticket.objects.filter(user=self.request.user)
    
        


class CreateMessageByAdminView(CreateAPIView):
    queryset = TicketMessage.objects.all()
    permission_classes = [IsAuthenticated, GroupPermission("SupportPanel", "SuperUser")]
    serializer_class = TicketMessageSerializer


    def perform_create(self, serializer):
        serializer.save(
            sender = self.request.user
        )
        



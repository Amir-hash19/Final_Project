from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Ticket, TicketMessage
from account.permissions import GroupPermission
from .serializers import TicketSerializer




class CreateTicketView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TicketSerializer


    def perform_create(self, serializer):
        serializer.save(
            user=self.request.user
        )
                  




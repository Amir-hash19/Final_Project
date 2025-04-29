from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import Ticket, TicketMessage






class TicketSerializer(ModelSerializer):
    class Meta:
        model = Ticket
        fields = "__all__"
        read_only_fields = ("user", "status")



class TicketMessageSerializer(ModelSerializer):
    class Meta:
        model = TicketMessage
        fields = "__all__"
        read_only_fields = ("sender", )
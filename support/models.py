from django.db import models
from account.models import CustomUser
from bootcamp.models import Bootcamp




class Ticket(models.Model):
    TICKET_STATUS_CHOICES = (
        ("pending", "Pending"),
        ("answered", "Answered"),
        ("notanswered", "NotAnswered"),
        ("closed", "Closed")
    )

    title = models.CharField(max_length=100)
    description = models.TextField()
    user = models.ForeignKey(to=CustomUser, on_delete=models.CASCADE)
    bootcamp = models.ForeignKey(to=Bootcamp, null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=TICKET_STATUS_CHOICES)

    def __str__(self):
        return self.title




class TicketMessage(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(to=CustomUser, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    attachment = models.FileField(upload_to='ticket_attachments/', null=True, blank=True)

    def __str__(self):
        return self.created_at

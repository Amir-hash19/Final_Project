from django.db.models.signals import post_save
from .models import Ticket, TicketMessage
from django.dispatch import receiver
from account.models import CustomUser
from .tasks import send_notify_admin_for_ticket


@receiver(post_save, sender=Ticket)
def norify_admin_for_ticket(sender, created, instance, **kwargs):
    if created:
        admin_panel = CustomUser.objects.filter(group="SupportPanel").first()
        phone = admin_panel.phone
        name = admin_panel.last_name

        send_notify_admin_for_ticket.delay(phone, name)
        
        


      

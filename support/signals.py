from django.db.models.signals import post_save
from .models import Ticket, TicketMessage
from django.dispatch import receiver
from account.models import CustomUser
from .tasks import send_notify_admin_for_ticket



@receiver(post_save, sender=Ticket)
def norify_admin_for_ticket(sender, created, instance, **kwargs):
    if created:
        admins = CustomUser.objects.filter(groups__name="SupportPanel")

        if admins.exists():
            for admin in admins:
                phone = admin.phone
                name = admin.last_name

                send_notify_admin_for_ticket.delay(phone, name)
        else:
            print("no admin found for sending notification")

       

        
        
        


      

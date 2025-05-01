from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Sum
from .models import *
from .tasks import call_user_for_invoice_task







@receiver(post_save, sender=Payment)
def update_ispaid(sender, instance, **kwargs):
    invoice = instance.invoice
    total_paid = invoice.payments.aggregate(total=models.Sum('amount'))['total'] or 0

    if total_paid >= invoice.amount:
        invoice.is_paid = True
        invoice.save()


        




@receiver(post_save, sender=Invoice)
def notify_invoice_for_client(sender, created ,instance, **kwargs):
    if created:
        user = instance.client
        amount = instance.amount
        user_phone = str(user.phone)
        last_name = user.last_name
    
    call_user_for_invoice_task.delay(user_phone, last_name, amount)





@receiver(post_save, sender=Payment)
def create_transctioon_on_payment_verified(sender, instance, created, **kwargs):

    if instance.is_verified and not created:

        Transaction.objects.create(
            user=instance.user,
            amount=instance.amount,
            description=f"Payment for Invoice ID {instance.invoice.id}",
            transaction_type='debit',
            is_verified=instance.is_verified
        )
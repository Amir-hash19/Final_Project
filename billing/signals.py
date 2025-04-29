from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Sum
from .models import *


@receiver(post_save, sender=Payment)
def update_ispaid(sender, instance, **kwargs):
    invoice = instance.invoice
    total_paid = invoice.payments.aggregate(total=models.Sum('amount'))['total'] or 0

    if total_paid >= invoice.amount:
        invoice.is_paid = True
        invoice.save()


        





from celery import shared_task
from .models import Invoice, Payment
from kavenegar import KavenegarAPI, APIException, HTTPException
from django.conf import settings
from django.utils.timezone import now


api = KavenegarAPI(settings.KAVENEGAR_API_KEY)


@shared_task(bind=True, max_retries=3, default_retry_delay=5, ignore_result=True)
def notify_when_deadline(self, phone, name):
    from django.utils.timezone import localdate
    today = localdate()
    
    invoices = Invoice.objects.filter(is_paid=False, deadline__lt=today)
    
    for invoice in invoices:
        user = invoice.client
        phone = str(user.phone_number) 
        name = invoice.client.first_name
        
        message = f"Dear {name}, {message} Amount: {invoice.amount} /:"    
        
        params = {
            "receptor":phone,
            "message":message,
            "sender":"2000660110"
        }
        try:
            response = api.sms_send(params)
            if response.get('status') != 200:
                raise Exception("SMS sending failed.")
        except Exception as e:
            raise self.retry(exc=e)    
    return f"SMS notifications sent successfully"





@shared_task(bind=True, max_retries=3, default_retry_delay=10, ignore_result=True)
def call_user_for_invoice_task(self, phone, last_name, amount=None):
    try:
        if amount is None:
            message = f"Hi {last_name} new Invoice from kelassor created for you please check your panel"
        else:
            message = f"{last_name} new Invoice for kelassor created for you --> {amount} <--"    
        
        params = {
            "receptor":phone,
            "message":message,
            "sender":"2000660110"
        }
        response = api.sms_send(params)
        
    except Exception as e:
        raise self.retry(exc=e)
    return f"SMS sent SuccessFully!"
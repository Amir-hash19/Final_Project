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
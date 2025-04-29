from celery import shared_task
from django.conf import settings
from celery.exceptions import Retry
from kavenegar import KavenegarAPI, APIException, HTTPException


api = KavenegarAPI(settings.KAVENEGAR_API_KEY)


@shared_task(bind=True, max_retries=3, default_retry_delay=3, ignore_result=True)
def send_notify_admin_for_ticket(self, phone, name):
    try:
        message = f"Some One just sent Ticket Please Check Your adminpanel {name}"

        params = {
            "receptor":phone,
            "message":message,
            "sender":"2000660110"
        }
        response = api.sms_send(params)
        return response
    
    except (APIException ,HTTPException) as e:
        print("Something sent wrong!")
    try:
        self.retry(exc=e) 
    except Retry:
        return {"status":"failed", "reason":str(e)}  




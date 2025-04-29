from celery import shared_task
from django.conf import settings
from celery.exceptions import Retry
from datetime import timedelta
from django.utils import timezone
from .models import Ticket
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





@shared_task(bind=True, max_retries=2, default_retry_delay=3, ignore_result=True)
def check_update_status_tickets():
    one_week_ago = timezone.now() - timedelta(weeks=1)


    tickets = Ticket.objects.filter(created_at=one_week_ago, status="pending", ticketmessage__isnull=True)

    for ticket in tickets:
        ticket.status = "notanswered"
        ticket.save()
        print("the tickets status is updated Successfully!")

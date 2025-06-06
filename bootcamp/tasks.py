from celery import shared_task
from django.conf import settings
from celery.exceptions import Retry
import time
from kavenegar import KavenegarAPI, APIException, HTTPException
from .models import SMSLog

api = KavenegarAPI(settings.KAVENEGAR_API_KEY)






@shared_task(bind=True, max_retries=3, default_retry_delay=5, ignore_result=True)
def send_sms_to_user(self, phone, full_name):#ارسال پیام به یوزر که ایا درخواستش قبول شده یا نه 
    try:
        message = f"{full_name} The result of your registration just came! check website please !"
        params = {
            "receptor":phone,
            "message":message,
            "sender":"2000660110"
        }
        response = api.sms_send(params)

        SMSLog.objects.create(
            phone_number = phone,
            full_name = full_name,
            status = "Success",
            response_message = str(response)
        )
        return response
    
    except (APIException ,HTTPException) as e:
        SMSLog.objects.create(
            phone_number = phone,
            full_name = full_name,
            status = "Unsuccess",
            response_message = str(e)
        )
        try:
            self.retry(exc=e) 
        except Retry:
            return {"status":"failed", "reason":str(e)}    






@shared_task(bind=True, max_retries=3, default_retry_delay=5, ignore_result=True)
def send_SMS_to_admin_for_registration(self, phone_admin, name_admin):
    try:
        message = f"hi {name_admin} SomeOne Just Registred for BootCamp Please Check!"

        params = {
            'receptor':phone_admin,
            "message":message,
            "sender":"2000660110"
        }
        response = api.sms_send(params)    
        return {"status": "success", "response": response}
    

    except (APIException, HTTPException) as e:
        try:
            self.retry(exc=e)
        except Retry:
            return {"status":"failed", "reason":str(e)}
             





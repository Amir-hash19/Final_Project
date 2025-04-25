from django.conf import settings
from celery import shared_task
import random 
import redis
from django.core.cache import cache
from kavenegar import KavenegarAPI

api = KavenegarAPI(settings.KAVENEGAR_API_KEY)



@shared_task
def send_otp_task(phone):
    otp = str(random.randint(100000, 999999))

    cache.set(f"otp:{phone}", otp, timeout=180)


    try:
        params = {
            "sender": 2000660110,
            "receptor":phone,
            "message":f"Your OTP code is: {otp}"
        }
        response = api.sms_send(params)
        print(f"OTP for {phone}: {otp}, SMS sent successfully")
    except Exception as e:
        print(f"Error sending OTP: {str(e)}")    

    return otp    


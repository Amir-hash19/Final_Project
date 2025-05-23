from django.conf import settings
from celery import shared_task
import random 
import redis
from django.core.cache import cache
from kavenegar import KavenegarAPI
import os



api = KavenegarAPI(settings.KAVENEGAR_API_KEY)

@shared_task
def send_otp_task(self, phone):
    otp = str(random.randint(100000, 999999))
    cache.set(f"otp:{phone}", otp, timeout=180)
    cache_key = f"otp{phone}"


    try:
        params = {
            "sender": "2000660110",
            "receptor":phone,
            "message":f"Your OTP code is: {otp}"
        }
        response = api.sms_send(params)
        print(f"OTP for {phone}: {otp}, SMS sent successfully, this is only credit for 2minutes!")
        return otp
    except Exception as e:
        raise self.retry(exc=e)
    finally:
        cache.delete(cache_key)
        

    





@shared_task(bind=True, max_retries=3, default_retry_delay=60)  
def send_welcome_sms_task(self, user_phone_number, first_name):
    api_key = os.getenv('KAVENEGAR_API_KEY')  
    client = KavenegarAPI(api_key)
    cache_key = f"welcome_sms:{user_phone_number}"

    try:
        params = {
            'receptor': user_phone_number,  
            'message': f"Welcome and tnx for SigningUp {first_name}",  
            'sender': "2000660110",  
        }
        response = client.sms_send(params)  
        return response
    except Exception as e:
        raise self.retry(exc=e)
    finally:
        cache.delete(cache_key)
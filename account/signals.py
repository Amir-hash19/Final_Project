from django.db.models.signals import post_save
from .models import CustomUser
from .tasks import send_welcome_sms_task
from django.dispatch import receiver
import logging




logger = logging.getLogger(__name__)


@receiver(post_save, sender=CustomUser)
def send_welcome_notify(sender, created, instance, **kwargs):
    if created:
        first_name = instance.first_name
        user_phone_number = str(instance.phone)

        try:
            send_welcome_sms_task.delay(first_name, user_phone_number)
        except Exception as e:
            logger.error(f"Error sending welcome SMS: {str(e)}")
            print(f"Error sending welcome SMS: {str(e)}") 
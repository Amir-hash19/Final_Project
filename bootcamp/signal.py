from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from .models import BootcampRegistration, Bootcamp
from .tasks import send_sms_to_user, send_SMS_to_admin_for_registration




@receiver(pre_save, sender=BootcampRegistration)
def notify_user(sender, instance, **kwargs):
    if instance.pk:
        previous = BootcampRegistration.objects.get(id=instance.pk)
        if previous.status != instance.status:
            phone = str(instance.phone_number)
            full_name = str(instance.volunteer)

            send_sms_to_user.delay(phone, full_name)


            

@receiver(post_save, sender=BootcampRegistration)#الان اگه رکوردی ثبت بشه به ادمین خبر داده میشه تا بررسی کنه 
def call_admin_for_Registration(sender, created, instance, **kwargs):
    if created:
        phone_admin = str(instance.reviewed_by.phone)
        name_admin = instance.reviewed_by.last_name
        try:
            send_SMS_to_admin_for_registration.delay(phone_admin, name_admin)#مشکل داره
            
            return f"the message has been sent to {name_admin}"
        except Exception:
            return f"Something went wrong!"
        





@receiver(post_save, sender=BootcampRegistration)
def check_capacity_bootcamp(sender, instance, created, **kwargs):
    if not created and instance.status == "approved":
        bootcamp = instance.bootcamp
        if bootcamp.capacity > 0:
            bootcamp.capacity -= 1
            bootcamp.save()


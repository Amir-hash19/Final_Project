from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from .models import BootcampRegistration, Bootcamp
from .tasks import send_sms_to_user




@receiver(pre_save, sender=BootcampRegistration)
def notify_user(sender, instance, **kwargs):
    if instance.pk:
        previous = BootcampRegistration.objects.get(id=instance.pk)
        if previous.status != instance.status:
            phone = str(instance.phone_number)
            full_name = str(instance.volunteer)

            send_sms_to_user.delay(phone, full_name)


            




@receiver(post_save, sender=BootcampRegistration)
def check_capacity_bootcamp(sender, instance, created, **kwargs):
    if not created and instance.status == "approved":
        bootcamp = instance.bootcamp
        if bootcamp.capacity > 0:
            bootcamp.capacity -= 1
            bootcamp.save()


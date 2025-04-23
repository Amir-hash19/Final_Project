from phonenumber_field.modelfields import PhoneNumberField
from account.models import CustomUser
from django.db import models




class BootcampCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)


    def __str__(self):
        return f"{self.name}"





class Bootcamp(models.Model):

    BOOTCAMP_STATUS_CHOICES=(
        ("draft", "Draft"),
        ("registering", "Registering"),
        ("currently", "Currently"),
        ("finished","Finished"),
        ("canceled", "Canceled")
    )                         
    
    title = models.CharField(max_length=100)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=20, choices=BOOTCAMP_STATUS_CHOICES, default="draft")
    is_online = models.BooleanField(default=True)
    capacity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    instructor = models.ManyToManyField(to=CustomUser, related_name="teachers")
    category = models.ForeignKey(to=BootcampCategory, on_delete=models.CASCADE, null=True ,related_name="bootcamp_list")
    created_at = models.DateField(auto_now_add=True)
    hours = models.CharField(max_length=50)
    days = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)


    def __str__(self):
        return self.title
    


class BootcampRegistration(models.Model):
    volunteer = models.ForeignKey(to=CustomUser, on_delete=models.CASCADE, name="student")
    bootcamp = models.ForeignKey(to=Bootcamp, on_delete=models.CASCADE, name="bootcamp")

    PAYMENT_STATUS_CHOICES = (
        ("installment_pay", "Installment_Pay"),
        ("check", "Check"),
        ("safte", "Safte"),
    )
    payment_type = models.CharField(max_length=30, choices=PAYMENT_STATUS_CHOICES, default="check")
    registered_at = models.DateTimeField(auto_now_add=True)

    REGISTRATION_STATUS_CHOICES = (
    ('pending', 'Pending'),
    ('reviewing', 'Reviewing'),
    ('approved', 'Approved'),
    ('rejected', 'Rejected'),
)
    status = models.CharField(max_length=20, choices=REGISTRATION_STATUS_CHOICES, default="pending")
    reviewed_at = models.DateTimeField(null=True, blank=True)
    reviewed_by = models.ForeignKey(to=CustomUser, null=True, blank=True, on_delete=models.SET_NULL, related_name='reviewed_enrollments')
    comment = models.TextField(blank=True)
    phone_number = PhoneNumberField(region='IR', unique=True)
    slug = models.SlugField(unique=True)


    def __str__(self):
        return f"{self.status}"
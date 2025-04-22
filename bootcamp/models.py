from django.db import models
from account.models import CustomUser




class BootcampCategory(models.Model):
    bootcamp = models.ForeignKey(to="Bootcamp", on_delete=models.CASCADE)
    slug = models.SlugField(unique=True)


    def __str__(self):
        return f"{self.bootcamp}"





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
    capacity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=3)
    instructor = models.ForeignKey(to=CustomUser, on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey("BootcampCategory", on_delete=models.SET_NULL, null=True)
    created_at = models.DateField(auto_now_add=True)
    hours = models.CharField(max_length=50)


    def __str__(self):
        return self.title
    


class BootcampRegistration(models.Model):

    REGISTRATION_STATUS_CHOICES = (
    ('pending', 'Pending'),
    ('reviewing', 'Reviewing'),
    ('approved', 'Approved'),
    ('rejected', 'Rejected'),
)

    student = models.ForeignKey(to=CustomUser, on_delete=models.CASCADE, name="student")
    bootcamp = models.ForeignKey(Bootcamp, on_delete=models.CASCADE, name="bootcamp")
    registered_at = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=REGISTRATION_STATUS_CHOICES)
    comment = models.TextField(blank=True)


    def __str__(self):
        return self.comment

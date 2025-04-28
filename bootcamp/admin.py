from django.contrib import admin
from .models import BootcampCategory, Bootcamp, BootcampRegistration, SMSLog



admin.site.register(Bootcamp)
admin.site.register(BootcampCategory)
admin.site.register(BootcampRegistration)
admin.site.register(SMSLog)

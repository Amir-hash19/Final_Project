from django.contrib import admin
from .models import CustomUser



@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ("first_name", "email", "gender")
    list_filter = ("date_created",)
    search_fields = ("username", "email")
    



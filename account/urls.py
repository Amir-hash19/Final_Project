from django.urls import path
from .views import RegisterAccountView



urlpatterns = [
    path("register-user/", RegisterAccountView.as_view(), name="register-account"),
]

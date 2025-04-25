from django.urls import path
from .views import RegisterAccountView, SendOTPView, VerifyOTPView



urlpatterns = [
    path("register-user/", RegisterAccountView.as_view(), name="register-account"),
    path("get-otp/", SendOTPView.as_view(), name="OTP-code"),
    path("verify-otp/", VerifyOTPView.as_view(), name="verify-otp"),
]

from django.urls import path
from .views import RegisterAccountView, SendOTPLogInView, VerifyOTPView



urlpatterns = [
    path("register-user/", RegisterAccountView.as_view(), name="register-account"),
    path("get-otp/", SendOTPLogInView.as_view(), name="OTP-code"),
    path("verify-otp/", VerifyOTPView.as_view(), name="verify-otp"),
]

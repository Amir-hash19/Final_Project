from django.urls import path
from .views import (RegisterAccountView, SendOTPLogInView, VerifyOTPView, LogoutView,
AssignSupportPanelPermissionView, DeleteSupportAdminView, DeleteAccount, AccountDetailsView, ListSupportAccountView)




urlpatterns = [
    path("register-user/", RegisterAccountView.as_view(), name="register-account"),
    path("get-otp/", SendOTPLogInView.as_view(), name="OTP-code"),
    path("verify-otp/", VerifyOTPView.as_view(), name="verify-otp"),
    path("logout/", LogoutView.as_view(), name="logout-account"),
    path("user/<int:pk>/assign-permission/", AssignSupportPanelPermissionView.as_view(), name="create-superuser-supportpanel"),
    path("delete-account/<int:pk>", DeleteSupportAdminView.as_view(), name="delete-account"),#کاربر پنل یا سوپریوزر
    path("delete-account-normal/", DeleteAccount.as_view(), name="delete-account-normal"),# کاربر عادی
    path("account-info/", AccountDetailsView.as_view(), name="account-info"),#کاربر عادی
    path("list-accounts-panel/", ListSupportAccountView.as_view(), name="list-support-account")#دیدن اکانت های پنل سایت
]


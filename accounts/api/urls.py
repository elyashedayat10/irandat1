from django.urls import path

from .views import (LoginApiView, LogoutApiView, PasswordChange,
                    SendOtpApiView, VerifyApiView, AdminListApiView, AdminCreateApiView, AdminDeleteApiView)

urlpatterns = [
    path("send_otp/", SendOtpApiView.as_view()),
    path("verify/", VerifyApiView.as_view()),
    path("login/", LoginApiView.as_view()),
    path("logout/", LogoutApiView.as_view()),
    path("password_change/", PasswordChange.as_view()),
    path("admin_list/", AdminListApiView.as_view()),
    path("admin_create/", AdminCreateApiView.as_view()),
    path("admin_delete/<int:pk>/", AdminDeleteApiView.as_view()),
]

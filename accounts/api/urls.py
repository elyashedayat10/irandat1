from django.urls import path

from .views import (SendOtpApiView,
                    VerifyApiView,
                    LoginApiView)

urlpatterns = [
    path("send_otp/", SendOtpApiView.as_view()),
    path("verify/", VerifyApiView.as_view()),
    path("login/", LoginApiView.as_view()),
]

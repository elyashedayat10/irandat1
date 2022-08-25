from django.urls import path

from .views import (
    AdminCreateApiView,
    AdminDeleteApiView,
    AdminListApiView,
    LoginApiView,
    LogoutApiView,
    MakeAdminUserApiView,
    MakeNormalUserApiView,
    PasswordChange,
    PasswordReset,
    PasswordResetVerify,
    SendOtpApiView,
    UserListApiView,
    VerifyApiView,
    UpdateUserApiView,
)

urlpatterns = [
    path("send_otp/", SendOtpApiView.as_view()),
    path("verify/", VerifyApiView.as_view()),
    path("login/", LoginApiView.as_view()),
    path("logout/", LogoutApiView.as_view()),
    path("password_change/", PasswordChange.as_view()),
    path("admin_list/", AdminListApiView.as_view()),
    path("admin_create/", AdminCreateApiView.as_view()),
    path("admin_delete/<int:pk>/", AdminDeleteApiView.as_view()),
    path("password_reset/", PasswordReset.as_view()),
    path("password_reset_verify/", PasswordResetVerify.as_view()),
    path("user_list/", UserListApiView.as_view()),
    path("make_admin/<int:pk>/", MakeAdminUserApiView.as_view()),
    path("make_normal/<int:pk>/", MakeNormalUserApiView.as_view()),
    path("update_user/", UpdateUserApiView.as_view()),
]

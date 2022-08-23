from django.urls import path

from .views import (
    GuideApiView,
    GuideCreateApiView,
    NotificationListApiView,
    SettingApiView,
    SettingCreateApiView,
)

urlpatterns = [
    path("", GuideApiView.as_view()),
    path("create/", GuideCreateApiView.as_view()),
    path("setting_create/", SettingCreateApiView.as_view()),
    path("setting/", SettingApiView.as_view()),
    path("notification_list/", NotificationListApiView.as_view()),
]

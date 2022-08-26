from django.urls import path

from .views import (
    GuideApiView,
    GuideCreateApiView,
    NotificationListApiView,
    SettingApiView,
    SettingCreateApiView,
    NotificationDetailApiViewApiView,
    NotificationUpdateAllApiView,
    NotificationDeleteApiViewApiView,
)

urlpatterns = [
    path("", GuideApiView.as_view()),
    path("create/", GuideCreateApiView.as_view()),
    path("setting_create/", SettingCreateApiView.as_view()),
    path("setting/", SettingApiView.as_view()),
    path("notification_list/", NotificationListApiView.as_view()),
    path("notification_update_all/", NotificationUpdateAllApiView.as_view()),
    path("notification_detail/<int:pk/>", NotificationDetailApiViewApiView.as_view()),
    path("notification_delete/<int:pk>/", NotificationDeleteApiViewApiView.as_view()),
]

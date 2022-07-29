from django.urls import path

from .views import PanelView, SettingCreateView, SettingView

app_name = "config"
urlpatterns = [
    path("", PanelView.as_view(), name="panel"),
    path("setting/", SettingView.as_view(), name="setting"),
    path("setting_create/", SettingCreateView.as_view(), name="create"),
]

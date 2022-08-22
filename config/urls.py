from django.urls import include, path

from config.api.urls import urlpatterns

from .views import PanelView, SettingCreateView, SettingView

app_name = "config"
urlpatterns = [
    path("", PanelView.as_view(), name="panel"),
    path("setting/", SettingView.as_view(), name="setting"),
    path("setting_create/", SettingCreateView.as_view(), name="create"),
    path("api/", include(urlpatterns)),
]

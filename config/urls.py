from django.urls import path, include

from .views import PanelView, SettingCreateView, SettingView
from config.api.urls import urlpatterns

app_name = "config"
urlpatterns = [
    path("", PanelView.as_view(), name="panel"),
    path("setting/", SettingView.as_view(), name="setting"),
    path("setting_create/", SettingCreateView.as_view(), name="create"),
    path('api/', include(urlpatterns)),
]

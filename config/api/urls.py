from django.urls import path
from .views import GuideApiView, GuideCreateApiView, SettingCreateApiView, SettingApiView

urlpatterns = [
    path('', GuideApiView.as_view()),
    path('create/', GuideCreateApiView.as_view()),
    path('setting_create/', SettingCreateApiView.as_view()),
    path('setting/', SettingApiView.as_view()),
]

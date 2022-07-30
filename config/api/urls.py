from django.urls import path
from .views import GuideApiView, GuideCreateApiView

urlpatterns = [
    path('', GuideApiView.as_view()),
    path('create/', GuideCreateApiView.as_view()),
]

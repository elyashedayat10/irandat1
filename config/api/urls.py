from django.urls import path
from .views import GuideApiView, GuideCreateApiView

urlpatterns = [
    path('', GuideApiView.as_view()),
    path('create/', GuideApiView.as_view()),
]

from django.urls import path

from .views import (
    CategoryCreateAPIView,
    CategoryDeleteApiView,
    CategoryListApiView,
    CategoryUpdateApiView,
)

urlpatterns = [
    path("list/", CategoryListApiView.as_view()),
    path("create/", CategoryCreateAPIView.as_view()),
    path("update/<int:pk>/", CategoryUpdateApiView.as_view()),
    path("delete/<int:pk>/", CategoryDeleteApiView.as_view()),
]

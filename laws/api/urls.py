from django.urls import path

from .views import (
    LawCategoryListApiView,
    LawCreateApiView,
    LawDeleteApiView,
    LawListApiView,
    LawUpdateApiView,
    SearchApiView,
)

urlpatterns = [
    path("<int:pk>/", LawCategoryListApiView.as_view()),
    path("list/", LawListApiView.as_view()),
    path("create/", LawCreateApiView.as_view()),
    path("delete/<int:pk>/", LawDeleteApiView.as_view()),
    path("update/<int:pk>/", LawUpdateApiView.as_view()),
    path("search/", SearchApiView.as_view()),
]

from django.urls import path

from .views import NoteCreateApiView, NoteDeleteApiView, NoteUpdateApiView

urlpatterns = [
    path("create/", NoteCreateApiView.as_view()),
    path("update/<int:pk>/", NoteUpdateApiView.as_view()),
    path("delete/<int:pk>/", NoteDeleteApiView.as_view()),
]

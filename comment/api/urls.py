from django.urls import path
from .views import (
    CommentCreateApiView,
    CommentUpdateApiView,
    CommentDeleteApiView
)

urlpatterns = [
    path('create/', CommentCreateApiView.as_view()),
    path('update/<int:pk>/', CommentUpdateApiView.as_view()),
    path('delete/<int:pk>/', CommentDeleteApiView.as_view()),

]

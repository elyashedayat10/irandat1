from django.urls import path

from .views import (CommentCreateApiView, CommentDeleteApiView,
                    CommentUpdateApiView,NotConfirmedCommentApiView,ConfirmCommentApiView)

urlpatterns = [
    path('create/', CommentCreateApiView.as_view()),
    path('update/<int:pk>/', CommentUpdateApiView.as_view()),
    path('delete/<int:pk>/', CommentDeleteApiView.as_view()),
    path('not_confirmed/', NotConfirmedCommentApiView.as_view()),
    path('confirme/<int:pk>/', ConfirmCommentApiView.as_view()),

]

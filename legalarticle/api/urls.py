from django.urls import path

from .views import (LegaArticleApiView, LegaArticleCreateApiView,
                    LegaArticleDestroyApiView, LegaArticleUpdateApiView, LegalArticleDetailView)

urlpatterns = [
    path('create/', LegaArticleCreateApiView.as_view()),
    path('update/<int:pk>/', LegaArticleUpdateApiView.as_view()),
    path('delete/<int:pk>/', LegaArticleDestroyApiView.as_view()),
    path('<int:pk>/', LegaArticleApiView.as_view()),
    path('detail/<int:pk>/', LegalArticleDetailView.as_view()),
]

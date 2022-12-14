from django.urls import path

from .views import (
    AllHitsListApiView,
    ArticleHitApiView,
    DisLikeApiView,
    FavoriteApiView,
    LegaArticleApiView,
    LegaArticleCreateApiView,
    LegaArticleDestroyApiView,
    LegaArticleUpdateApiView,
    LegalArticleDetailView,
    MostViewedArticleApiView,
)

urlpatterns = [
    path("create/", LegaArticleCreateApiView.as_view()),
    path("update/<int:pk>/", LegaArticleUpdateApiView.as_view()),
    path("delete/<int:pk>/", LegaArticleDestroyApiView.as_view()),
    path("<int:pk>/", LegaArticleApiView.as_view()),
    path("hits_list/", AllHitsListApiView.as_view()),
    path("favorite/", FavoriteApiView.as_view()),
    path("hits_list/<int:pk>/", AllHitsListApiView.as_view()),
    path("detail/<int:pk>/", LegalArticleDetailView.as_view(),name="detail"),
    path("detail_hit/<int:pk>/", ArticleHitApiView.as_view()),
    path("dislike/", DisLikeApiView.as_view()),
    path("most_viewd/", MostViewedArticleApiView.as_view()),
]

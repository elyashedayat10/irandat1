from django.urls import path

from .views import (
    LawCategoryListApiView,
    LawCreateApiView,
    LawDeleteApiView,
    LawListApiView,
    LawUpdateApiView,
    SearchApiView,
    ChapterCreateApiView,
    ChapterUpdateApiView,
    ChapterDeleteApiView,
    LawChapterListApiView,
)

urlpatterns = [
    path("<int:pk>/", LawCategoryListApiView.as_view()),
    path("list/", LawListApiView.as_view()),
    path("create/", LawCreateApiView.as_view()),
    path("delete/<int:pk>/", LawDeleteApiView.as_view()),
    path("update/<int:pk>/", LawUpdateApiView.as_view()),
    path("search/", SearchApiView.as_view()),
    path("chapter_create/", ChapterCreateApiView.as_view()),
    path("chapter_update/<int:pk>/", ChapterUpdateApiView.as_view()),
    path("chapter_delete/<int:pk>/", ChapterDeleteApiView.as_view()),
    path("law_chapters/<int:pk>/", LawChapterListApiView.as_view()),
]

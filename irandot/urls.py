from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("category/", include("categories.urls", namespace="category")),
    path("config/", include("config.urls", namespace="config")),
    path("accounts/", include("accounts.urls", namespace="accounts")),
    path("laws/", include("laws.urls", namespace="laws")),
    path("article/", include("legalarticle.urls", namespace='legal')),
    path("comment/", include("comment.urls", namespace='comment')),
    path("ticcket/", include("tickets.urls", namespace='ticket')),
    path("note/", include("notes.urls", namespace='notes')),
]
if settings.DEBUG:
    urlpatterns = urlpatterns + static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
    urlpatterns = urlpatterns + static(
        settings.STATIC_URL, document_root=settings.STATIC_ROOT
    )

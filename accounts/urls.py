from django.urls import include, path

from accounts.api.urls import urlpatterns

from .views import g

app_name = "accounts"

urlpatterns = [
    path("api/", include(urlpatterns)),
    path("", g),
]

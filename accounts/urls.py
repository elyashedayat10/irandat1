from django.urls import include, path

from accounts.api.urls import urlpatterns



app_name = "accounts"

urlpatterns = [
    path("api/", include(urlpatterns)),
]
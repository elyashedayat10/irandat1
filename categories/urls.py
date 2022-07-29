from django.urls import include, path

from categories.api.urls import urlpatterns


app_name = "category"

urlpatterns = [
    path("api/", include(urlpatterns)),
]

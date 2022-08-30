from django.urls import include, path

from config.api.urls import urlpatterns


app_name = "config"
urlpatterns = [
    path("api/", include(urlpatterns)),
]

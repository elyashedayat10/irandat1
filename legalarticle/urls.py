from django.urls import include, path

from legalarticle.api.urls import urlpatterns



app_name = "legal"
urlpatterns = [
    path("api/", include(urlpatterns)),
]

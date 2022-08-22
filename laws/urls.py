from django.urls import include, path

app_name = "laws"
from laws.api.urls import urlpatterns

urlpatterns = [
    path("api/", include(urlpatterns)),
]

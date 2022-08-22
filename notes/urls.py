from django.urls import include, path

from notes.api.urls import urlpatterns

app_name = "notes"

urlpatterns = [path("api/", include(urlpatterns))]

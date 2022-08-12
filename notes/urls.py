from django.urls import path, include
from notes.api.urls import urlpatterns

app_name = "notes"

urlpatterns = [
    path("api/", include(urlpatterns))
]

from django.urls import include, path

from tickets.api.urls import urlpatterns

app_name = "tickets"
urlpatterns = [path("api/", include(urlpatterns))]

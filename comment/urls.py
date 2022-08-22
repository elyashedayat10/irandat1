from django.urls import include, path

from comment.api.urls import urlpatterns

app_name = "comment"

urlpatterns = [path("api/", include(urlpatterns))]

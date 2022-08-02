from django.urls import path, include
from tickets.api.urls import urlpatterns

app_name = 'tickets'
urlpatterns = [
    path('api/', include(urlpatterns))

]

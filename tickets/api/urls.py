from django.urls import path

from .views import (AnswerCreateApiView, TicketCloseApiView,
                    TicketCreateApiView, TicketDetailApiView,
                    UserTicketApiView, TickerListApiView)

urlpatterns = [
    path('', UserTicketApiView.as_view()),
    path('list/', TickerListApiView.as_view()),
    path('<int:ticket_id>/', TicketDetailApiView.as_view()),
    path('close/<int:ticket_id>/', TicketCloseApiView.as_view()),
    path('create/', TicketCreateApiView.as_view()),
    path('answer/<int:ticket_id>/', AnswerCreateApiView.as_view()),

]

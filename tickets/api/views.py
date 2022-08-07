from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAdminUser
from rest_framework.generics import GenericAPIView, ListAPIView, RetrieveAPIView, CreateAPIView
from rest_framework.response import Response

from ..models import Answer, Ticket
from .serializers import AnswerSerializer, TicketSerializer


class UserTicketApiView(ListAPIView):
    serializer_class = TicketSerializer

    def get_queryset(self):
        user_ticket = self.request.user.tickets.all()
        return user_ticket


class TickerListApiView(ListAPIView):
    serializer_class = TicketSerializer
    queryset = Ticket.objects.all()
    permission_classes = [IsAdminUser]


class TicketDetailApiView(RetrieveAPIView):
    serializer_class = AnswerSerializer

    def get_queryset(self):
        ticket_id = self.kwargs.get('pk')
        queryset = Answer.objects.filter(ticket_id=ticket_id)
        return queryset


class TicketCreateApiView(CreateAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer


class AnswerCreateApiView(GenericAPIView):
    serializer_class = AnswerSerializer

    def post(self, request, *args, **kwargs):
        ticket_id = kwargs.get('ticket_id')
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            if request.user.is_admin:
                serializer.save(ticket_id=ticket_id, from_who='user')
            else:
                serializer.save(ticket_id=ticket_id, from_who='admin')
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TicketCloseApiView(GenericAPIView):

    def get(self, request, *args, **kwargs):
        ticket_id = kwargs.get('ticket_id')
        ticket_obj = Ticket.objects.get(id=ticket_id)
        ticket_obj.status = "بسته شده"
        ticket_obj.save()
        return Response(data={
            'message': 'تیکت با موفقیت بسته شد',
        }, status=status.HTTP_200_OK)

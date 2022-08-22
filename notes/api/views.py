from rest_framework.generics import CreateAPIView, DestroyAPIView, UpdateAPIView
from rest_framework.response import Response

from ..models import Note
from .serializers import NoteSerializers


class NoteCreateApiView(CreateAPIView):
    queryset = Note.objects.all()
    serializer_class = NoteSerializers

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response({"message": "note created", "data": response.data})


class NoteUpdateApiView(UpdateAPIView):
    queryset = Note.objects.all()
    serializer_class = NoteSerializers

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        return Response({"message": "note updated", "data": response.data})


class NoteDeleteApiView(DestroyAPIView):
    queryset = Note.objects.all()
    serializer_class = NoteSerializers

    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        return Response({"message": "note deleted", "data": response.data})

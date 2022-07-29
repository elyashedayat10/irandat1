from requests import Response

from .serializers import CommentSerializer
from ..models import Comment
from rest_framework.generics import CreateAPIView, UpdateAPIView, DestroyAPIView
from .permissions import OwnerPermission
from rest_framework.permissions import IsAuthenticated


class CommentCreateApiView(CreateAPIView):
    permission_classes = [IsAuthenticated, ]
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CommentUpdateApiView(UpdateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    lookup_field = 'pk'
    lookup_url_kwarg = 'pk'
    permission_classes = [OwnerPermission, ]

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)


class CommentDeleteApiView(DestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    lookup_field = 'pk'
    lookup_url_kwarg = 'pk'
    permission_classes = [OwnerPermission, ]

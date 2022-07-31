from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     UpdateAPIView, ListAPIView, GenericAPIView)
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from ..models import Comment
from .permissions import OwnerPermission
from .serializers import CommentSerializer
from rest_framework import status

class CommentCreateApiView(CreateAPIView):
    permission_classes = [IsAuthenticated, ]
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class NotConfirmedCommentApiView(ListAPIView):
    permission_classes = [IsAdminUser, ]
    queryset = Comment.objects.filter(confirmed=False)
    serializer_class = CommentSerializer


class CommentUpdateApiView(UpdateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    lookup_field = 'pk'
    lookup_url_kwarg = 'pk'
    permission_classes = [OwnerPermission, ]

    def perform_update(self, serializer):
        serializer.save(user=self.request.user, confirmed=False)


class CommentDeleteApiView(DestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    lookup_field = 'pk'
    lookup_url_kwarg = 'pk'
    permission_classes = [OwnerPermission, ]


    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)
        return Response({
            'status': 200,
            'message': 'obj deleted',
        })


class ConfirmCommentApiView(GenericAPIView):
    permission_classes = [IsAdminUser, ]

    def get(self, request, *args, **kwargs):
        comment_id = kwargs.get('pk')
        comment_obj = get_object_or_404(Comment, id=comment_id)
        comment_obj.confirmed = True
        comment_obj.save()
        content={'message': 'comment confirmed'}
        return Response(content,status=status.HTTP_200_OK)

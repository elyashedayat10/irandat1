from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from pusher import Pusher
from rest_framework import status
from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    GenericAPIView,
    ListAPIView,
    UpdateAPIView,
)
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from ..models import Comment
from .permissions import OwnerPermission
from .serializers import CommentSerializer
from .throttle import CustomUserRateThrottle

pusher = Pusher(
    app_id="1438811",
    key="05c8dc49c22fbb40bde3",
    secret="4d37a334eb4d651892f5",
    cluster="mt1",
    ssl=True,
)


class CommentCreateApiView(CreateAPIView):
    throttle_classes = [CustomUserRateThrottle]
    permission_classes = [
        IsAuthenticated,
    ]
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        pusher.trigger("irandat", "my-event", {"message": "کامنت جدیدی ثبت شده"})
        # subject = 'welcome to GFG world'
        # message = f'Hi {user.username}, thank you for registering in geeksforgeeks.'
        # email_from = settings.EMAIL_HOST_USER
        # recipient_list = [user.email, ]
        # send_mail(subject, message, email_from, recipient_list)

        serializer.save(user=self.request.user)


class CommentUpdateApiView(UpdateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    lookup_field = "pk"
    lookup_url_kwarg = "pk"
    permission_classes = [
        OwnerPermission,
    ]

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)


class CommentDeleteApiView(DestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    lookup_field = "pk"
    lookup_url_kwarg = "pk"
    permission_classes = [
        OwnerPermission,
        IsAdminUser,
    ]

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)
        return Response(
            {
                "status": 200,
                "message": "obj deleted",
            }
        )


class CommentListApiView(ListAPIView):
    permission_classes = [
        IsAdminUser,
    ]
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

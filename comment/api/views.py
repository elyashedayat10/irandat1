from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView,
    UpdateAPIView,
)
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from config.models import Notification

from ..models import Comment
from .permissions import OwnerPermission
from .serializers import CommentSerializer
from .throttle import CustomUserRateThrottle


class CommentCreateApiView(CreateAPIView):
    throttle_classes = [CustomUserRateThrottle]
    permission_classes = [
        IsAuthenticated,
    ]
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        Notification.objects.create(
            text=f" دیدگاه جدید:{self.request.user.first_name} {self.request.user.last_name}"
        )
        # subject = 'welcome to GFG world'
        # message = f'Hi {user.username}, thank you for registering in geeksforgeeks.'
        # email_from = settings.EMAIL_HOST_USER
        # recipient_list = [user.email, ]
        # send_mail(subject, message, email_from, recipient_list)


class CommentUpdateApiView(UpdateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [
        OwnerPermission,
    ]

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)


class CommentDeleteApiView(DestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [
        OwnerPermission,
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

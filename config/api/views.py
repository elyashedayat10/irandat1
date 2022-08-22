from rest_framework import status
from rest_framework.generics import CreateAPIView, GenericAPIView, ListAPIView
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from ..models import Guide, Setting, Notification
from .serializers import GuideSerializer, SettingSerializer, NotificationSerializer


class GuideApiView(GenericAPIView):
    serializer_class = GuideSerializer

    def get(self, request, *args, **kwargs):
        serializer = self.serializer_class(Guide.load()).data
        return Response(data=serializer, status=status.HTTP_200_OK)


class GuideCreateApiView(CreateAPIView):
    queryset = Guide.load()
    serializer_class = GuideSerializer
    permission_classes = [IsAdminUser, ]


class SettingCreateApiView(CreateAPIView):
    queryset = Setting.load()
    serializer_class = SettingSerializer
    permission_classes = [IsAdminUser, ]


class SettingApiView(GenericAPIView):
    serializer_class = SettingSerializer

    def get(self, request, *args, **kwargs):
        serializer = self.serializer_class(Setting.load()).data
        return Response(data=serializer, status=status.HTTP_200_OK)


class NotificationListApiView(ListAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [IsAdminUser, ]

    def list(self, request, *args, **kwargs):
        response = super(NotificationListApiView, self).list(request, *args, **kwargs)
        unread_count = self.get_queryset().filter(read=False).count()
        return Response(
            data={
                "data": response.data,
                "unread_count": unread_count,
            }
        )

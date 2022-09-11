from rest_framework import status
from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    GenericAPIView,
    ListAPIView,
    RetrieveAPIView,
)
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from ..models import Guide, Notification, Setting
from .serializers import GuideSerializer, NotificationSerializer, SettingSerializer


# class GuideApiView(GenericAPIView):
#     serializer_class = GuideSerializer
#
#     def get(self, request, *args, **kwargs):
#         serializer = self.serializer_class(Guide.load()).data
#         return Response(data=serializer, status=status.HTTP_200_OK)


# class GuideCreateApiView(CreateAPIView):
#     # queryset = Guide.load()
#     serializer_class = GuideSerializer
#     permission_classes = [
#         IsAdminUser,
#     ]


# class SettingCreateApiView(CreateAPIView):
#     queryset = Setting.load()
#     serializer_class = SettingSerializer
#     permission_classes = [
#         IsAdminUser,
#     ]


# class SettingApiView(GenericAPIView):
#     serializer_class = SettingSerializer
#
#     def get(self, request, *args, **kwargs):
#         serializer = self.serializer_class(Setting.load()).data
#         return Response(data=serializer, status=status.HTTP_200_OK)


class NotificationListApiView(ListAPIView):
    queryset = Notification.objects.filter(read=True)
    serializer_class = NotificationSerializer
    permission_classes = [
        IsAdminUser,
    ]

    def list(self, request, *args, **kwargs):
        response = super(NotificationListApiView, self).list(request, *args, **kwargs)
        unread_list = Notification.objects.filter(read=False)
        return Response(
            data={
                "read_list": response.data,
                "unread_list": self.serializer_class(unread_list, many=True).data,
                "unread_count": unread_list.count(),
            }
        )


class NotificationDetailApiViewApiView(GenericAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer

    def get(self, request, *args, **kwargs):
        pk = self.kwargs.get("pk")
        notif_obj = Notification.objects.get(pk=pk)
        serializer = self.serializer_class(notif_obj).data
        notif_obj.read = True
        notif_obj.save()
        return Response(
            data={
                "message": "notif detail",
                "data": serializer,
            }
        )


class NotificationUpdateAllApiView(ListAPIView):
    queryset = Notification.objects.filter(read=False)
    serializer_class = NotificationSerializer
    permission_classes = [
        IsAdminUser,
    ]

    def list(self, request, *args, **kwargs):
        super(NotificationUpdateAllApiView, self).list(request, *args, **kwargs)
        self.get_queryset().update(read=True)
        return Response(data={"message": "all the notif updated"})


class NotificationDeleteApiViewApiView(DestroyAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [
        IsAdminUser,
    ]

    def get_renderer_context(self):
        render = super().get_renderer_context()
        render["message"] = "notif deleted"
        return render

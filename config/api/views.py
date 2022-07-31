from rest_framework.generics import GenericAPIView, CreateAPIView
from .serializers import GuideSerializer
from ..models import Guide
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework import status


class GuideApiView(GenericAPIView):
    serializer_class = GuideSerializer

    def get(self, request, *args, **kwargs):
        serializer = self.serializer_class(Guide.load()).data
        return Response(data=serializer, status=status.HTTP_200_OK)


class GuideCreateApiView(CreateAPIView):
    queryset = Guide.load()
    serializer_class = GuideSerializer
    permission_classes = [IsAdminUser, ]

from rest_framework.generics import ListAPIView, CreateAPIView
from .serializers import GuideSerializer
from ..models import Guide
from rest_framework.permissions import IsAdminUser


class GuideApiView(ListAPIView):
    # queryset = Guide.load()
    # serializer_class = GuideSerializer
    pass

class GuideCreateApiView(CreateAPIView):
    pass
    # queryset = Guide.load()
    # serializer_class = GuideSerializer
    # permission_classes = [IsAdminUser, ]

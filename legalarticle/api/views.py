from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, UpdateAPIView)
from rest_framework.response import Response

from ..models import LegalArticle
from .serializers import LegalArticleSerializer


class LegaArticleApiView(ListAPIView):
    serializer_class = LegalArticleSerializer
    queryset = LegalArticle.objects.all()

    def get_queryset(self):
        queryset = super(LegaArticleApiView, self).get_queryset()
        return queryset.filter(law_id=self.kwargs.get('pk'))

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return Response({
            'status': 201,
            'message': 'legal list',
            'data': response.data
        })


class LegaArticleCreateApiView(CreateAPIView):
    serializer_class = LegalArticleSerializer
    queryset = LegalArticle.objects.all()

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response({
            "status": 201,
            'message': 'legal created',
            'data': response.data
        })


class LegaArticleUpdateApiView(UpdateAPIView):
    serializer_class = LegalArticleSerializer
    queryset = LegalArticle.objects.all()

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        return Response({
            "status": 200,
            'message': 'legal updated',
            'data': response.data
        })


class LegaArticleDestroyApiView(DestroyAPIView):
    serializer_class = LegalArticleSerializer
    queryset = LegalArticle.objects.all()

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)
        return Response({
            "status": 200,
            'message': 'legal deleted',
        })

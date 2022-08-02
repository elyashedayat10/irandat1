from django.db.models import Sum
from django.db.models.functions import TruncDate
from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, UpdateAPIView, RetrieveAPIView)
from rest_framework.response import Response

from ..models import LegalArticle, ArticleHit
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
            'message': 'legal list',
            'data': response.data
        })


class LegaArticleCreateApiView(CreateAPIView):
    serializer_class = LegalArticleSerializer
    queryset = LegalArticle.objects.all()

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response({
            'message': 'legal created',
            'data': response.data
        })


class LegaArticleUpdateApiView(UpdateAPIView):
    serializer_class = LegalArticleSerializer
    queryset = LegalArticle.objects.all()

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        return Response({
            'message': 'legal updated',
            'data': response.data
        })


class LegaArticleDestroyApiView(DestroyAPIView):
    serializer_class = LegalArticleSerializer
    queryset = LegalArticle.objects.all()

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)
        return Response({
            'message': 'legal deleted',
        })


class LegalArticleDetailView(RetrieveAPIView):
    serializer_class = LegalArticleSerializer
    queryset = LegalArticle.objects.all()

    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        article = self.get_object()
        ip_address = self.request.user.ip_address
        if ip_address not in article.hits.all():
            article.hits.add(ip_address)
        return Response({
            'data': response.data
        })

# class LegalArticleList(ListAPIView):
#
#     def get_queryset(self):
#         article = self.get_object()
#         ArticleHit.objects.filter(article_id=article.id).annotate(Sum('ip_address')).annotate(
#             hours=TruncDate('created'))

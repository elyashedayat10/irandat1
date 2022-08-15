from re import L

import httpagentparser
from django.db.models import F
from rest_framework import status
from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, UpdateAPIView, GenericAPIView,
                                     get_object_or_404)
from rest_framework.response import Response

from categories.models import Category
from legalarticle.models import LegalArticle, ArticleHit
from ..models import Law
from .serializers import LawSerializer
from legalarticle.api.serializers import LegalArticleSerializer
from rest_framework.permissions import IsAdminUser


class LawListApiView(ListAPIView):
    queryset = Law.objects.all()
    serializer_class = LawSerializer

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return Response({
            'status': 200,
            'message': 'law list',
            'data': response.data
        })


class LawCategoryListApiView(ListAPIView):
    queryset = Law.objects.all()
    serializer_class = LawSerializer

    def get_queryset(self):
        # queryset = super(LawCategoryListApiView, self).get_queryset()
        category_id = self.kwargs.get("id")
        laws_list = Law.objects.filter(category_id=category_id)
        category_obj = get_object_or_404(Category, id=category_id)
        if category_obj.get_descendant_count() >= 1:
            category_list = category_obj.get_descendants(include_self=False)
            laws_list = Law.objects.filter(category__in=category_list)
        return laws_list

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return Response({
            'status': 200,
            'message': 'law base on category ',
            'data': response.data
        })


class LawCreateApiView(CreateAPIView):
    queryset = Law.objects.all()
    serializer_class = LawSerializer
    permission_classes = [IsAdminUser, ]

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response({
            'status': 201,
            'message': 'obj created',
            'data': response.data
        })


class LawUpdateApiView(UpdateAPIView):
    queryset = Law.objects.all()
    serializer_class = LawSerializer
    permission_classes = [IsAdminUser, ]

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        return Response({
            'status': 200,
            'message': 'obj updated',
            'data': response.data
        })


class LawDeleteApiView(DestroyAPIView):
    queryset = Law.objects.all()
    serializer_class = LawSerializer
    permission_classes = [IsAdminUser, ]

    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        return Response({
            'status': 200,
            'message': 'obj deleted',
        })


class SearchApiView(GenericAPIView):
    def get(self, request, *args, **kwargs):
        query_params = request.query_params.get('q')
        law_obj = Law.objects.filter(title__icontains=query_params)
        article_obj = LegalArticle.objects.filter(description__icontains=query_params).order_by("hits")
        agent = request.META["HTTP_USER_AGENT"]
        print(agent)
        operating_system = httpagentparser.detect(agent)['platform']["name"]
        for article in article_obj:
            ArticleHit.objects.create(article=article, operating_system=operating_system,
                                      previous_page=request.META.get('HTTP_REFERER'),
                                      location=""
                                      )
        context = {
            'law': LawSerializer(law_obj, many=True).data,
            'article': LegalArticleSerializer(article_obj, many=True).data,
        }
        return Response(data=context, status=status.HTTP_200_OK)

from django.db.models import Sum, Count, Q
from django.db.models.functions import TruncDate, TruncMinute, TruncTime, TruncHour, TruncMonth, TruncYear, TruncDay
from django.shortcuts import get_object_or_404
from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, UpdateAPIView, RetrieveAPIView, GenericAPIView)
from rest_framework.response import Response
from ..models import LegalArticle, ArticleHit
from .serializers import LegalArticleSerializer
from datetime import datetime, timedelta


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


from rest_framework.permissions import IsAdminUser
import httpagentparser


class LegalArticleDetailView(RetrieveAPIView):
    serializer_class = LegalArticleSerializer
    queryset = LegalArticle.objects.all()

    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        article = self.get_object()
        agent = request.META["HTTP_USER_AGENT"]
        operating_system = httpagentparser.detect(agent)['platform']["name"]
        print(request.META.get('HTTP_REFERER'))
        ArticleHit.objects.create(article=article, operating_system=operating_system,
                                  previous_page=request.META.get('HTTP_REFERER'),
                                  location=""
                                  )
        return Response({
            'data': response.data
        })


# class LegalArticleList(ListAPIView):
#
#     def get_queryset(self):
#         article = self.get_object()
#         ArticleHit.objects.filter(article_id=article.id).annotate(Sum('ip_address')).annotate(
#             hours=TruncDate('created'))

from .serializers import HitsCountSer
import datetime


class ArticleHitApiView(GenericAPIView):
    def get(self, request, pk):
        today = datetime.date.today()
        yesterday = today - timedelta(days=1)
        today_views = ArticleHit.objects.filter(created__date=today).count()
        yesterday_views = ArticleHit.objects.filter(created__date=yesterday).count()
        minutes = ArticleHit.objects.values(time=TruncMinute('created')).annotate(
            count=Count('article')).order_by('time')
        hours = ArticleHit.objects.values(time=TruncHour('created')).annotate(count=Count('article')).order_by('time')
        day = ArticleHit.objects.values(time=TruncDay('created')).annotate(count=Count('article')).order_by('time')
        months = ArticleHit.objects.values(time=TruncMonth('created')).annotate(count=Count('article')).order_by(
            'time')
        year = ArticleHit.objects.values(time=TruncYear('created')).annotate(count=Count('article')).order_by('time')
        last_7_day = ArticleHit.objects.filter(created__date__gte=(today - timedelta(days=7))).aggregate(Count('id'))[
            "id__count"]
        last_30_day = ArticleHit.objects.filter(created__date__gte=(today - timedelta(days=30))).aggregate(Count('id'))[
            "id__count"]
        last_60_day = ArticleHit.objects.filter(created__date__gte=(today - timedelta(days=60))).aggregate(Count('id'))[
            "id__count"]
        last_90_day = ArticleHit.objects.filter(created__date__gte=(today - timedelta(days=90))).aggregate(Count('id'))[
            "id__count"]
        # result = ArticleHit.objects.aggregate(
        #     total=Count('id'),
        #     today=Count('id', filter=Q(created__date=day)),
        #     yesterday=Count('id', filter=Q(created__date__gte=(today - timedelta(days=1)))),
        #     last_7_day=Count('id', filter=Q(created__date__gte=(today - timedelta(days=7)))),
        #     last_30_day=Count('id', filter=Q(created__date__gte=(today - timedelta(days=30)))),
        #     last_60_day=Count('id', filter=Q(created__date__gte=(today - timedelta(days=60)))),
        #     last_90_day=Count('id', filter=Q(created__date__gte=(today - timedelta(days=90)))),
        # )
        context = {"last_7_day": last_7_day, "minutes": minutes, "hours": hours,
                   "day": day, "months": months, "year": year, "today": today_views,
                   "yesterday": yesterday_views, "last_30_day": last_30_day, "last_60_day": last_60_day,
                   "last_90_day": last_90_day}
        return Response(data=context)


class AllHitsListApiView(ListAPIView):
    serializer_class = HitsCountSer
    permission_classes = [IsAdminUser,]

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        queryset =  ArticleHit.objects.all()
        if pk:
            queryset = ArticleHit.objects.filter(article_id=pk)
        return queryset

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return Response({
            "data": response.data,
            "message": "hits views"
        })


# class HitsByArticleView(ListAPIView):
#     serializer_class = HitsCountSer
#
#     def get_queryset(self):
#         pk = self.kwargs.get('pk')
#         legal = ArticleHit.objects.filter(article_id=pk)
#         return legal
#
#     def list(self, request, *args, **kwargs):
#         response = super().list(request, *args, **kwargs)
#         return Response({
#             "data": response.data,
#             "message": "hits base on article"
#         })

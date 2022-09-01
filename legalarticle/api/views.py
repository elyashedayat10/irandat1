from datetime import datetime, timedelta

from django.db.models import Count, Q, Sum
from django.db.models.functions import (
    TruncDate,
    TruncDay,
    TruncHour,
    TruncMinute,
    TruncMonth,
    TruncTime,
    TruncYear,
)
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    GenericAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ..models import ArticleHit, Dislike, Favorite, LegalArticle
from .serializers import (
    DislikeSerializer,
    FavoriteSerializer,
    LegalArticleDetailSerializer,
    LegalArticleSerializer,
)


class LegaArticleApiView(ListAPIView):
    serializer_class = LegalArticleDetailSerializer
    queryset = LegalArticle.objects.all()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context

    def get_queryset(self):
        queryset = super(LegaArticleApiView, self).get_queryset()
        return queryset.filter(law_id=self.kwargs.get("pk"))

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return Response({"message": "legal list", "data": response.data})


class LegaArticleCreateApiView(CreateAPIView):
    serializer_class = LegalArticleDetailSerializer
    queryset = LegalArticle.objects.all()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response({"message": "legal created", "data": response.data})


class LegaArticleUpdateApiView(UpdateAPIView):
    serializer_class = LegalArticleDetailSerializer
    queryset = LegalArticle.objects.all()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        return Response({"message": "legal updated", "data": response.data})


class LegaArticleDestroyApiView(DestroyAPIView):
    serializer_class = LegalArticleDetailSerializer
    queryset = LegalArticle.objects.all()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)
        return Response(
            {
                "message": "legal deleted",
            }
        )


import httpagentparser
from rest_framework.permissions import IsAdminUser


class LegalArticleDetailView(RetrieveAPIView):
    serializer_class = LegalArticleDetailSerializer
    queryset = LegalArticle.objects.all()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context

    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        article = self.get_object()
        agent = request.META["HTTP_USER_AGENT"]
        operating_system = httpagentparser.detect(agent)["platform"]["name"]
        print(request.META.get("HTTP_REFERER"))
        ArticleHit.objects.create(
            article=article,
            operating_system=operating_system,
            previous_page=request.META.get("HTTP_REFERER"),
            location="",
        )
        return Response({"data": response.data})


import datetime

from .serializers import HitsCountSer


class ArticleHitApiView(GenericAPIView):
    def get(self, request, pk):
        today = datetime.date.today()
        yesterday = today - timedelta(days=1)
        today_views = ArticleHit.objects.filter(created__date=today).count()
        yesterday_views = ArticleHit.objects.filter(created__date=yesterday).count()
        minutes = (
            ArticleHit.objects.values(time=TruncMinute("created"))
            .annotate(count=Count("article"))
            .order_by("time")
        )
        hours = (
            ArticleHit.objects.values(time=TruncHour("created"))
            .annotate(count=Count("article"))
            .order_by("time")
        )
        day = (
            ArticleHit.objects.values(time=TruncDay("created"))
            .annotate(count=Count("article"))
            .order_by("time")
        )
        months = (
            ArticleHit.objects.values(time=TruncMonth("created"))
            .annotate(count=Count("article"))
            .order_by("time")
        )
        year = (
            ArticleHit.objects.values(time=TruncYear("created"))
            .annotate(count=Count("article"))
            .order_by("time")
        )
        last_7_day = ArticleHit.objects.filter(
            created__date__gte=(today - timedelta(days=7))
        ).aggregate(Count("id"))["id__count"]
        last_30_day = ArticleHit.objects.filter(
            created__date__gte=(today - timedelta(days=30))
        ).aggregate(Count("id"))["id__count"]
        last_60_day = ArticleHit.objects.filter(
            created__date__gte=(today - timedelta(days=60))
        ).aggregate(Count("id"))["id__count"]
        last_90_day = ArticleHit.objects.filter(
            created__date__gte=(today - timedelta(days=90))
        ).aggregate(Count("id"))["id__count"]
        # result = ArticleHit.objects.aggregate(
        #     total=Count('id'),
        #     today=Count('id', filter=Q(created__date=day)),
        #     yesterday=Count('id', filter=Q(created__date__gte=(today - timedelta(days=1)))),
        #     last_7_day=Count('id', filter=Q(created__date__gte=(today - timedelta(days=7)))),
        #     last_30_day=Count('id', filter=Q(created__date__gte=(today - timedelta(days=30)))),
        #     last_60_day=Count('id', filter=Q(created__date__gte=(today - timedelta(days=60)))),
        #     last_90_day=Count('id', filter=Q(created__date__gte=(today - timedelta(days=90)))),
        # )
        context = {
            "last_7_day": last_7_day,
            "minutes": minutes,
            "hours": hours,
            "day": day,
            "months": months,
            "year": year,
            "today": today_views,
            "yesterday": yesterday_views,
            "last_30_day": last_30_day,
            "last_60_day": last_60_day,
            "last_90_day": last_90_day,
        }
        return Response(data=context)


class AllHitsListApiView(ListAPIView):
    serializer_class = HitsCountSer
    permission_classes = [
        IsAdminUser,
    ]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context

    def get_queryset(self):
        pk = self.kwargs.get("pk")
        queryset = ArticleHit.objects.all()
        if pk:
            queryset = ArticleHit.objects.filter(article_id=pk)
        return queryset

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return Response({"data": response.data, "message": "hits views"})


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


class FavoriteApiView(GenericAPIView):
    permission_classes = [
        IsAuthenticated,
    ]

    def get(self, request, *args, **kwargs):
        liked_list = request.user.likes.all().values_list("id", flat=True)
        liked_articles = LegalArticle.objects.filter(id__in=liked_list)
        serializer = LegalArticleSerializer(
            instance=liked_articles, many=True, context={"request": request}
        )
        context = {
            "message": "لیست لایک های کاربر",
            "data": serializer.data,
        }
        return Response(data=context, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = FavoriteSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            like_obj = Favorite.objects.filter(
                user=request.user, article_id=serializer.validated_data["article"]
            )
            if like_obj.exists():
                like_obj.delete()
                context = {
                    "is_done": True,
                    "message": "با موفقیت از like ها حذف شد",
                }
            else:
                serializer.save(user=request.user)
                context = {
                    "is_done": True,
                    "message": "با موفقیت به like ها اضافه شد",
                    "data": serializer.data,
                }

            return Response(data=context, status=status.HTTP_200_OK)
        context = {
            "is_done": False,
            "message": "خطا در انجام عملیات",
        }
        return Response(data=context, status=status.HTTP_400_BAD_REQUEST)


class DisLikeApiView(GenericAPIView):
    permission_classes = [
        IsAuthenticated,
    ]

    def get(self, request, *args, **kwargs):
        diliked_list = request.user.dislikes.all().values_list("id", flat=True)
        diliked_articles = LegalArticle.objects.filter(id__in=diliked_list)
        serializer = LegalArticleSerializer(
            instance=diliked_articles, many=True, context={"request": request}
        )
        context = {
            "message": "لیست dislike کاربر",
            "data": serializer.data,
        }
        return Response(data=context, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = DislikeSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            like_obj = Dislike.objects.filter(
                user=request.user, article_id=serializer.validated_data["article"]
            )
            if like_obj.exists():
                like_obj.delete()
                context = {
                    "is_done": True,
                    "message": "با موفقیت از dislike ها حذف شد",
                }
            else:
                serializer.save(user=request.user)
                context = {
                    "is_done": True,
                    "message": "با موفقیت به dislike ها اضافه شد",
                    "data": serializer.data,
                }

            return Response(data=context, status=status.HTTP_200_OK)
        context = {
            "is_done": False,
            "message": "خطا در انجام عملیات",
        }
        return Response(data=context, status=status.HTTP_400_BAD_REQUEST)


class MostViewedArticleApiView(GenericAPIView):
    def get(self, request, *args, **kwargs):
        legal_article_obj = LegalArticle.objects.annotate(count=Count('hits__id')).order_by('-count')[:10]
        serializer = LegalArticleSerializer(legal_article_obj, many=True).data
        return Response(
            data={"data": serializer},
            status=status.HTTP_200_OK
        )

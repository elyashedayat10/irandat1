from re import L

import httpagentparser
from django.db.models.functions import Greatest
from django.contrib.postgres.search import SearchQuery, SearchVector, TrigramSimilarity
from django.db.models import F
from rest_framework import status
from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    GenericAPIView,
    ListAPIView,
    UpdateAPIView,
    get_object_or_404,
)
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from categories.models import Category
from legalarticle.api.serializers import LegalArticleSerializer
from legalarticle.models import ArticleHit, LegalArticle

from ..models import Chapter, Law
from .serializers import ChapterSerializer, LawSerializer


class LawListApiView(ListAPIView):
    queryset = Law.objects.all()
    serializer_class = LawSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return Response({"status": 200, "message": "law list", "data": response.data})


class LawCategoryListApiView(ListAPIView):
    queryset = Law.objects.all()
    serializer_class = LawSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context

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
        return Response(
            {"status": 200, "message": "law base on category ", "data": response.data}
        )


class LawCreateApiView(CreateAPIView):
    queryset = Law.objects.all()
    serializer_class = LawSerializer
    permission_classes = [
        IsAdminUser,
    ]

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response(
            {"status": 201, "message": "obj created", "data": response.data}
        )

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context

    def perform_create(self, serializer):
        obj = serializer.save()
        Law.objects.filter(order__gte=obj.order).exclude(id=obj.id).update(order=F('order') + 1)


class LawUpdateApiView(UpdateAPIView):
    queryset = Law.objects.all()
    serializer_class = LawSerializer
    permission_classes = [
        IsAdminUser,
    ]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        return Response(
            {"status": 200, "message": "obj updated", "data": response.data}
        )

    def perform_update(self, serializer):
        order_number = serializer.validated_data['order']
        current_number = self.get_object().order
        if order_number > current_number:
            print("ali")
            if self.get_object().parent:
                category_obj = Law.objects.filter(parent=self.get_object().parent)
                category_obj.filter(order__gte=order_number).update(order=F('order') + 1)
            else:
                category_obj = Law.objects.filter(parent=None)
                print(category_obj)
                category_obj.filter(order__gte=order_number).update(order=F('order') + 1)
        elif order_number == current_number:
            pass
        else:
            print("reza")
            if self.get_object().parent:
                category_obj = Law.objects.filter(parent=self.get_object().parent)
                category_obj.filter(order__lte=order_number).update(order=F('order') - 1)
                print("elyas")
            else:
                print("ilghar")
                category_obj = Law.objects.filter(parent=None)
                category_obj.filter(order__lte=order_number).update(order=F('order') + 1)
        serializer.save()


class LawDeleteApiView(DestroyAPIView):
    queryset = Law.objects.all()
    serializer_class = LawSerializer
    permission_classes = [
        IsAdminUser,
    ]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)
        return Response(
            {
                "status": 200,
                "message": "obj deleted",
            }
        )


class SearchApiView(GenericAPIView):
    def get(self, request, *args, **kwargs):
        query_params = request.query_params.get("q")
        law_obj = (
            Law.objects.annotate(similarity=TrigramSimilarity("title", query_params))
            .filter(similarity__gt=0.2)
            .order_by("-similarity")
        )
        law_tags = (
            Law.objects.annotate(similarity=TrigramSimilarity("tags__name", query_params))
            .filter(similarity__gt=0.2)
            .order_by("-similarity")
        )
        article_obj = (
            LegalArticle.objects.annotate(
                similarity=TrigramSimilarity("description", query_params)
            )
            .filter(similarity__gt=0.2)
            .order_by("-similarity")
        )
        article_tags = (
            LegalArticle.objects.annotate(
                similarity=TrigramSimilarity("tags__name", query_params)
            )
            .filter(similarity__gt=0.2)
            .order_by("-similarity")
        )
        type_result = (
            LegalArticle.objects.annotate(
                similarity=TrigramSimilarity("_type", query_params)
            )
            .filter(similarity__gt=0.2)
            .order_by("-similarity")
        )
        type2_result = (
            LegalArticle.objects.annotate(
                similarity=TrigramSimilarity("_type2", query_params)
            )
            .filter(similarity__gt=0.2)
            .order_by("-similarity")
        )
        chapter_obj = (Chapter.objects.annotate(
            similarity=TrigramSimilarity("number", query_params)
        )
                       .filter(similarity__gt=0.2)
                       .order_by("-similarity")
                       )
        # agent = request.META["HTTP_USER_AGENT"]
        # operating_system = httpagentparser.detect(agent)['platform']["name"]
        # for article in article_obj:
        #     ArticleHit.objects.create(article=article, operating_system=operating_system,
        #                               previous_page=request.META.get('HTTP_REFERER'),
        #                               location=""
        #                               )
        context = {
            "law": LawSerializer(law_obj, many=True).data,
            "article": LegalArticleSerializer(article_obj, many=True).data,
            "chapter": ChapterSerializer(chapter_obj, many=True).data,
            "law_tags": LawSerializer(law_tags, many=True).data,
            "article_tags": LegalArticleSerializer(article_tags, many=True).data,
            "type_1": LegalArticleSerializer(type_result, many=True).data,
            "type2": LegalArticleSerializer(type2_result, many=True).data,
        }
        return Response(data=context, status=status.HTTP_200_OK)


class ChapterCreateApiView(CreateAPIView):
    serializer_class = ChapterSerializer
    queryset = Chapter.objects.all()
    permission_classes = [
        IsAdminUser,
    ]

    def create(self, request, *args, **kwargs):
        super().create(request, *args, **kwargs)
        return Response(
            data={"status": 201, "message": "chapter created", "data": request.data}
        )


class ChapterUpdateApiView(UpdateAPIView):
    serializer_class = ChapterSerializer
    queryset = Chapter.objects.all()
    permission_classes = [
        IsAdminUser,
    ]

    def update(self, request, *args, **kwargs):
        super().update(request, *args, **kwargs)
        return Response(
            data={"status": 200, "message": "chapter updated", "data": request.data}
        )

    def perform_update(self, serializer):
        order_number = serializer.validated_data['order']
        current_number = self.get_object().order
        if order_number > current_number:
            print("ali")
            if self.get_object().parent:
                category_obj = Chapter.objects.filter(parent=self.get_object().parent)
                category_obj.filter(order__gte=order_number).update(order=F('order') + 1)
            else:
                category_obj = Chapter.objects.filter(parent=None)
                print(category_obj)
                category_obj.filter(order__gte=order_number).update(order=F('order') + 1)
        elif order_number == current_number:
            pass
        else:
            print("reza")
            if self.get_object().parent:
                category_obj = Chapter.objects.filter(parent=self.get_object().parent)
                category_obj.filter(order__lte=order_number).update(order=F('order') - 1)
                print("elyas")
            else:
                print("ilghar")
                category_obj = Chapter.objects.filter(parent=None)
                category_obj.filter(order__lte=order_number).update(order=F('order') + 1)
        serializer.save()


class ChapterDeleteApiView(DestroyAPIView):
    serializer_class = ChapterSerializer
    queryset = Chapter.objects.all()
    permission_classes = [
        IsAdminUser,
    ]

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)
        return Response(
            data={
                "status": 200,
                "message": "chapter deleted",
            }
        )


class LawChapterListApiView(ListAPIView):
    serializer_class = ChapterSerializer

    def get_queryset(self):
        pk = self.kwargs.get("pk")
        chapter_list = Chapter.objects.filter(law_id=pk, parent=None)
        return chapter_list

    def list(self, request, *args, **kwargs):
        response = super(LawChapterListApiView, self).list(request, *args, **kwargs)
        return Response(
            data={
                "status": 200,
                "message": "chapter base on law",
                "data": response.data,
            }
        )

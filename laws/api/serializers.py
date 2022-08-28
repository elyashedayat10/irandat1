from rest_framework import serializers
from taggit.serializers import TaggitSerializer, TagListSerializerField

from legalarticle.api.serializers import LegalArticleSerializer

from ..models import Chapter, Law


class ChapterSerializer(serializers.ModelSerializer):
    articles = serializers.SerializerMethodField()
    children = serializers.SerializerMethodField()

    class Meta:
        model = Chapter
        fields = (
            "id",
            "number",
            "parent",
            "law",
            "order",
            "articles",
            "children",

        )
        read_only_fields = ["id", "children", "articles"]

    def get_children(self, obj):
        return ChapterSerializer(obj.get_children(), many=True).data

    def get_article(self, obj):
        return LegalArticleSerializer(obj.articles.all(), many=True).data


class LawSerializer(TaggitSerializer, serializers.ModelSerializer):
    article = serializers.SerializerMethodField()
    chapter = serializers.SerializerMethodField()
    tags = TagListSerializerField(allow_null=True)

    class Meta:
        model = Law
        fields = (
            "id",
            "title",
            "tags",
            "order",
            "category",
            "approved",
            "article",
            "published",
            "approval_authority",
            "chapter",
        )

        read_only_fields = (
            "article",
            "id",
            "chapter",
        )

    def get_article(self, obj):
        return LegalArticleSerializer(obj.articles.all(), many=True).data

    def get_chapter(self, obj):
        return ChapterSerializer(obj.chapters.all(), many=True).data

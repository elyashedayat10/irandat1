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
        return ChapterSerializer(obj.get_children().order_by("order"), many=True).data

    def get_articles(self, obj):
        return LegalArticleSerializer(obj.articles.all(), many=True).data

    # def validate_order(self, value):
    #     chapter_obj = Chapter.objects.filter(order=value)
    #     if chapter_obj.exists():
    #         raise serializers.ValidationError("this order already exists")
    #     return value


class ChapterPartialSerializer(serializers.ModelSerializer):
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

    def get_articles(self, obj):
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
        return ChapterSerializer(obj.chapters.all().order_by("order"), many=True).data

    # def validate_order(self, value):
    #     law_obj = Law.objects.filter(order=value)
    #     if law_obj.exists():
    #         raise serializers.ValidationError("this order already exists")
    #     return value


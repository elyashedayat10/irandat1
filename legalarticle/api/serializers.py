from rest_framework import serializers

from comment.api.serializers import CommentSerializer
from notes.api.serializers import NoteSerializers

from ..models import Dislike, Favorite, LegalArticle


class LegalArticleSerializer(serializers.ModelSerializer):
    comments = serializers.SerializerMethodField()
    notes = serializers.SerializerMethodField()
    # liked = serializers.SerializerMethodField()
    like_count = serializers.SerializerMethodField()

    class Meta:
        model = LegalArticle
        fields = (
            "id",
            "description",
            "approved",
            "law",
            "number",
            "comments",
            "notes",
            # "liked",
            "like_count",
        )
        read_only_fields = ("comments", "id", "notes", "liked", "like_count")

    def get_comments(self, obj):
        return CommentSerializer(obj.comments.all(), many=True).data

    def get_notes(self, obj):
        return NoteSerializers(obj.notes.all(), many=True).data

    # def get_liked(self, obj):
    #     if self.context['request'].user.is_authenticated():
    #         user = self.context['request'].user
    #         liked_list = user.likes.all().values_list('id', flat=True)
    #         if obj.id in liked_list:
    #             return True
    #         return False
    #     return False

    def get_like_count(self, obj):
        return obj.favorites.count()


class LegalArticleDetailSerializer(serializers.ModelSerializer):
    comments = serializers.SerializerMethodField()
    notes = serializers.SerializerMethodField()
    liked = serializers.SerializerMethodField()
    like_count = serializers.SerializerMethodField()

    class Meta:
        model = LegalArticle
        fields = (
            "id",
            "description",
            "approved",
            "law",
            "number",
            "comments",
            "notes",
            "liked",
            "like_count",
        )
        read_only_fields = ("comments", "id", "notes", "liked", "like_count")

    def get_comments(self, obj):
        return CommentSerializer(obj.comments.all(), many=True).data

    def get_notes(self, obj):
        return NoteSerializers(obj.notes.all(), many=True).data

    def get_liked(self, obj):
        user = self.context["request"].user
        if user.is_authenticated:
            liked_list = user.likes.all().values_list("id", flat=True)
            if obj.id in liked_list:
                return True
            return False
        return False

    def get_like_count(self, obj):
        return obj.favorites.count()


# class LegalArticleChartApiView(serializers.ModelSerializer):
#     count = serializers.IntegerField()
#     ip_address = serializers.CharField(source="ip_address__sum")
#     class Meta:
#         model = LegalArticle
#         fields = (
#             'id',
#             'description',
#             'approved',
#             'law',
#             'number',
#             'count',
#             'ip_address',
#         )

from ..models import ArticleHit


class HitsCountSer(serializers.ModelSerializer):
    class Meta:
        model = ArticleHit
        fields = (
            "article",
            "operating_system",
            "created",
            "previous_page",
            "location",
        )
        depth = 1


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = ("id", "user", "article")
        read_only_fields = ("id", "user")


class DislikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dislike
        fields = ("id", "user", "article")
        read_only_fields = ("id", "user")

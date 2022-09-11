from rest_framework import serializers

from notes.api.serializers import NoteSerializers

from ..models import ArticleHit, Dislike, Favorite, LegalArticle
from taggit.serializers import TaggitSerializer, TagListSerializerField
from comment.models import Comment
from comment.api.serializers import CommentSerializer


class LegalArticleSerializer(TaggitSerializer, serializers.ModelSerializer):
    comments = serializers.SerializerMethodField()
    notes = serializers.SerializerMethodField()
    # liked = serializers.SerializerMethodField()
    like_count = serializers.SerializerMethodField()
    dislike_count = serializers.SerializerMethodField()
    tags = TagListSerializerField(allow_null=True)

    class Meta:
        model = LegalArticle
        fields = (
            "id",
            "description",
            "approved",
            "law",
            "number",
            "chapter",
            "comments",
            "notes",
            "_type",
            "_type2",
            # "liked",
            "like_count",
            "dislike_count",
            "tags",
        )
        read_only_fields = (
            "comments",
            "id",
            "notes",
            "liked",
            "like_count",
            "dislike_count",
        )

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

    def get_dislike_count(self, obj):
        return obj.dislike.count()

    def get_comments(self, obj):
        comments_qs = Comment.objects.filter_parents_by_object(obj)
        return CommentSerializer(comments_qs, many=True).data


class LegalArticleDetailSerializer(TaggitSerializer, serializers.ModelSerializer):
    comments = serializers.SerializerMethodField()
    notes = serializers.SerializerMethodField()
    liked = serializers.SerializerMethodField()
    like_count = serializers.SerializerMethodField()
    dislike_count = serializers.SerializerMethodField()
    tags = TagListSerializerField(allow_null=True)

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
            "_type",
            "_type2",
            "liked",
            "like_count",
            "chapter",
            "dislike_count",
            "tags",
        )
        read_only_fields = (
            "comments",
            "id",
            "notes",
            "liked",
            "like_count",
            "dislike_count",
        )

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

    def get_dislike_count(self, obj):
        return obj.dislike.count()


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

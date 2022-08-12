from rest_framework import serializers
from notes.api.serializers import NoteSerializers
from comment.api.serializers import CommentSerializer

from ..models import LegalArticle


class LegalArticleSerializer(serializers.ModelSerializer):
    comments = serializers.SerializerMethodField()
    notes = serializers.SerializerMethodField()

    class Meta:
        model = LegalArticle
        fields = (
            'id',
            'description',
            'approved',
            'law',
            'number',
            'comments',
            "notes",
        )
        read_only_fields = ('comments', 'id', "notes",)

    def get_comments(self, obj):
        return CommentSerializer(obj.comments.all(), many=True).data

    def get_notes(self, obj):
        return NoteSerializers(obj.notes.all(), many=True).data


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
            'article',
            'operating_system',
            'created',
            'previous_page',
            'location',
        )
        depth = 1

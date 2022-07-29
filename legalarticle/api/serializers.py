from rest_framework import serializers

from comment.api.serializers import CommentSerializer

from ..models import LegalArticle


class LegalArticleSerializer(serializers.ModelSerializer):
    comments = serializers.SerializerMethodField()

    class Meta:
        model = LegalArticle
        fields = (
            'description',
            'approved',
            'law',
            'number',
            'comments',
        )
        read_only_fields = ('comments',)

    def get_comments(self, obj):
        return CommentSerializer(obj.comments.all(), many=True).data

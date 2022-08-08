from rest_framework import serializers

from comment.api.serializers import CommentSerializer

from ..models import LegalArticle


class LegalArticleSerializer(serializers.ModelSerializer):
    comments = serializers.SerializerMethodField()

    class Meta:
        model = LegalArticle
        fields = (
            'id',
            'description',
            'approved',
            'law',
            'number',
            'comments',
        )
        read_only_fields = ('comments', 'id',)

    def get_comments(self, obj):
        return CommentSerializer(obj.comments.all(), many=True).data


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
    count = serializers.IntegerField()
    time = serializers.DateTimeField()

    class Meta:
        model = ArticleHit
        fields = (
            'article',
            'operating_system',
            'created',
            'previous_page',
            'location',
            'count',
            'time',
        )

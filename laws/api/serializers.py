from rest_framework import serializers
from taggit.serializers import TaggitSerializer, TagListSerializerField

from legalarticle.api.serializers import LegalArticleSerializer

from ..models import Law


class LawSerializer(TaggitSerializer, serializers.ModelSerializer):
    article = serializers.SerializerMethodField()
    tags = TagListSerializerField(allow_null=True)

    class Meta:
        model = Law
        fields = (
            'id',
            'title',
            'tags',
            'category',
            'approved',
            'article',
            'published',
            "approval_authority",
        )

        read_only_fields = ('article', 'id',)

    def get_article(self, obj):
        return LegalArticleSerializer(obj.articles.all(), many=True).data

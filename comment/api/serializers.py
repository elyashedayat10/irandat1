from ..models import Comment
from rest_framework import serializers


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.phone_number')

    class Meta:
        model = Comment
        fields = (
            'parent',
            'user',
            'legal_article',
            'content',
        )
        read_only_fields = (
            'user',
        )

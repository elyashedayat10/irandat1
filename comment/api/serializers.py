from rest_framework import serializers

from ..models import Comment


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

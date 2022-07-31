from rest_framework import serializers

from ..models import Comment


class CommentSerializer(serializers.ModelSerializer):
    # user = serializers.CharField(source='user.phone_number')

    class Meta:
        model = Comment
        fields = (
            'id',
            'parent',
            'user',
            'legal_article',
            'content',
            'confirmed',
        )
        read_only_fields = (
            'user',
            'id',
            'confirmed',
        )

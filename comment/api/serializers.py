from rest_framework import serializers

from ..models import Comment
from accounts.api.serializers import UserMainSerializers


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = (
            'id',
            'parent',
            'user',
            'legal_article',
            'content',
            'created',
        )
        read_only_fields = (
            'user',
            'id',
            'created',
        )

    def get_user(self, obj):
        return UserMainSerializers(obj.user).data

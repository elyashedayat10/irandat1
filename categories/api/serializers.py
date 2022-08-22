from rest_framework import serializers

from ..models import Category


class CategorySerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = (
            "id",
            "parent",
            "title",
            "children",
            "order",
        )
        read_only_fields = ["id", "children"]

    def get_children(self, obj):
        return CategorySerializer(obj.get_children(), many=True).data

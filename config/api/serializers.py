from rest_framework import serializers
from ..models import Guide


class GuideSerializer(serializers.ModelSerializer):
    class Meta:
        model = Guide
        fields = ('text',)

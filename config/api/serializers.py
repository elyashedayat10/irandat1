from rest_framework import serializers

from ..models import Guide, Setting


class GuideSerializer(serializers.ModelSerializer):
    class Meta:
        model = Guide
        fields = ("text",)


class SettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Setting
        fields = ("title", "icon", "description")

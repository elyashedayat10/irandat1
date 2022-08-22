from rest_framework import serializers

from ..models import Guide, Setting, Notification


class GuideSerializer(serializers.ModelSerializer):
    class Meta:
        model = Guide
        fields = ("text",)


class SettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Setting
        fields = ("title", "icon", "description")


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = (
            'id',
            'text',
            'created',
        )

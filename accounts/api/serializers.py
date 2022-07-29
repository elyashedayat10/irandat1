from rest_framework import serializers


class PhoneSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=11)


class VerifySerializer(PhoneSerializer):
    code = serializers.CharField(max_length=6)
    fcm_token = serializers.CharField(max_length=1000)

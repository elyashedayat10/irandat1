from django.contrib.auth import get_user_model
from rest_framework import serializers

user = get_user_model()


class PhoneSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=11)
    first_name = serializers.CharField(max_length=125)
    last_name = serializers.CharField(max_length=125)
    password = serializers.CharField(max_length=11)

    def validate_password(self, value):
        if 4 <= len(value) <= 8:
            return value
        else:
            raise serializers.ValidationError("password at least must be 4 and eq than 8 ")


class VerifySerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=11)
    code = serializers.CharField(max_length=6)


class LoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=11)
    password = serializers.CharField()


class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(max_length=128)
    new_password = serializers.CharField(max_length=128)


class PasswordResetSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=12)


class PasswordResetVerifiedSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=100)
    new_password = serializers.CharField(max_length=128)
    code = serializers.CharField(max_length=10)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = user
        fields = ("id", "phone_number", "password")
        extra_kwargs = {"password": {"write_only": True}}
        read_only_fields = ("id",)


class UserMainSerializers(serializers.ModelSerializer):
    class Meta:
        model = user
        fields = (
            "id",
            "phone_number",
            "first_name",
            "last_name",
            "is_active",
            "joined",
            "description",
        )


class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = user
        fields = (
            "id",
            "phone_number",
            "first_name",
            "last_name",
            "email",
            "joined",
            "promoted_date",
            "description",
        )
        read_only_fields = ("id",)


class LoginSerializers(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class UpdateUserSerializers(serializers.ModelSerializer):
    class Meta:
        model = user
        fields = (
            "first_name",
            "last_name",
            "email",
        )


class DescriptionSerializer(serializers.Serializer):
    description = serializers.CharField()

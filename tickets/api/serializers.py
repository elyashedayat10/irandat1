from rest_framework import serializers

from ..models import Answer, Ticket
from accounts.api.serializers import UserMainSerializers


class TicketSerializer(serializers.ModelSerializer):
    body = serializers.CharField(write_only=True)
    user = serializers.SerializerMethodField()

    class Meta:
        model = Ticket
        fields = (
            'id',
            'user',
            'title',
            'type',
            'status',
            'closed_at',
            'code',
            'body',
        )
        read_only_fields = (
            'id',
            'user',
            'status',
            'closed_at',
            'code',
        )

    def create(self, validated_data):
        body = validated_data.pop('body')
        user = self.context['request'].user
        ticket = Ticket.objects.create(user=user, **validated_data)
        Answer.objects.create(body=body, from_who='user', ticket=ticket)
        return ticket

    def get_user(self, obj):
        return UserMainSerializers(obj.user).data


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = (
            'ticket',
            'from_who',
            'body',
            'created',
        )
        read_only_fields = (
            'ticket',
            'from_who',
            'created',
        )

from rest_framework import serializers

from ..models import Answer, Ticket


class TicketSerializer(serializers.ModelSerializer):
    body = serializers.CharField(write_only=True)

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
        ticket = Ticket.objects.create(**validated_data)
        Answer.objects.create(body=body, from_who='admin', ticket=ticket)
        return ticket


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


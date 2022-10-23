from rest_framework import serializers

from .models import Answer, Status, Ticket


#                      Status
class StatusSerializer(serializers.ModelSerializer):
    ticket_status = serializers.StringRelatedField(many=True, read_only=True)
    answer_status = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Status
        fields = ['id', 'status', 'ticket_status', 'answer_status']


#                         Ticket
class TicketSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    created_at = serializers.DateTimeField(read_only=True, format="%Y-%m-%d %H:%M:%S")
    status = serializers.StringRelatedField()
    answer = serializers.StringRelatedField(read_only=True, many=True)

    class Meta:
        model = Ticket
        fields = ['id', 'user', 'text', 'created_at', 'status', 'answer']


class TicketDetailSerializer(serializers.ModelSerializer):
    text = serializers.ReadOnlyField()
    user = serializers.StringRelatedField()
    created_at = serializers.DateTimeField(read_only=True, format="%Y-%m-%d %H:%M:%S")
    status = serializers.StringRelatedField()
    answer = serializers.StringRelatedField(many=True)

    class Meta:
        model = Ticket
        fields = ['id', 'user', 'text', 'created_at', 'status', 'answer']


#                            Answer
class AnswerSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    created_at = serializers.DateTimeField(read_only=True, format="%Y-%m-%d %H:%M:%S")
    ticket = serializers.SlugRelatedField(queryset=Ticket.objects.exclude(status__status="Solved"), slug_field="text")
    status = serializers.SlugRelatedField(queryset=Status.objects.all(), slug_field='status')

    class Meta:
        model = Answer
        fields = ['id', 'user', 'text', 'created_at', 'status', 'ticket']

    def create(self, validated_data):
        ticket = Ticket.objects.get(text=validated_data['ticket'])
        ticket.status = validated_data['status']
        ticket.save()
        return Answer.objects.create(**validated_data)


class AnswerDetailSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    created_at = serializers.DateTimeField(read_only=True, format="%Y-%m-%d %H:%M:%S")
    ticket = serializers.StringRelatedField(source='ticket.text')
    status = serializers.SlugRelatedField(queryset=Status.objects.all(), slug_field="status")

    class Meta:
        model = Answer
        fields = ['id', 'user', 'text', 'created_at', 'status', 'ticket']

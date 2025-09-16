from rest_framework import serializers

from notifications.models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = [
            'id',
            'user',
            'api_key',
            'type',
            'to',
            'subject',
            'body',
            'metadata',
            'status',
            'provider_response',
            'attempts',
            'created_at',
            'processed_at',
        ]
        read_only_fields = ['id', 'created_at', 'attempts', 'provider_response', 'status', 'user', 'api_key']

    def validate(self, attrs):
        type = attrs.get('type')
        if 'sms' or 'email' in type:
            return attrs
        raise serializers.ValidationError('تایپ یا sms و یا email باید باشد.')

    def create(self, validated_data):
        validated_data['attempts'] = 0
        validated_data['status'] = 'queued'

        return super().create(validated_data)

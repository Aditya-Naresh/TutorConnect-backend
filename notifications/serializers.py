from rest_framework import serializers
from .models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    unread_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Notification
        fields = [
            "id",
            "type",
            "message",
            "is_read",
            "timestamp",
            "unread_count",
        ]
        read_only_fields = [
            "id",
            "timestamp",
        ]

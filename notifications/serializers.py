from rest_framework import serializers
from .models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    unread_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Notification
        fields = [
            "id",
            "user",
            "type",
            "message",
            "is_read",
            "timestamp",
            "unread_count",
            "link",
        ]
        read_only_fields = [
            "id",
            "timestamp",
        ]

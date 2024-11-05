from rest_framework import serializers
from .models import Messages, ChatRooms
from django.contrib.auth import get_user_model

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["id", "full_name"]

    def get_full_name(self, obj):
        return obj.get_full_name()


class ChatroomSerializer(serializers.ModelSerializer):
    user1 = UserSerializer(read_only=True)
    user2 = UserSerializer(read_only=True)

    class Meta:
        model = ChatRooms
        fields = ["id", "user1", "user2"]


class MessageSerializer(serializers.ModelSerializer):
    chat_room = ChatroomSerializer(read_only=True)

    class Meta:
        model = Messages
        fields = [
            "id",
            "chat_room",
            "user",
            "content",
            "timestamp",
            "seen",
        ]

from rest_framework import serializers
from .models import Messages, ChatRooms
from accounts.models import User

class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["id", "full_name", "profile_pic"]

    def get_full_name(self, obj):
        return obj.get_full_name()


class ChatroomSerializer(serializers.ModelSerializer):
    user1 = UserSerializer(read_only=True)
    user2 = UserSerializer(read_only=True)
    unseen_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = ChatRooms
        fields = ["id", "user1", "user2", "unseen_count"]


class MessageSerializer(serializers.ModelSerializer):
    # chat_room = ChatroomSerializer(read_only=True)

    class Meta:
        model = Messages
        fields = [
            "id",
            "chat_room",
            "user",
            "content",
            "attachment",
            "timestamp",
            "seen",
        ]

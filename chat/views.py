from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from .models import Messages, ChatRooms
from django.contrib.auth import get_user_model

User = get_user_model()


class AttachmentMessageView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, *args, **kwargs):
        # Extract the required data
        user_id = request.data.get("user")
        other_user_id = request.data.get("other_user")
        attachment = request.FILES.get("attachment")
        user_ids = sorted([user_id, other_user_id])

        # Validate required fields
        if not user_ids or not attachment:
            return Response(
                {"error": "chat_room, user, and attachment are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            chat_room = ChatRooms.objects.get(
                user1_id=user_ids[0],
                user2_id=user_ids[1],
            )
            user = User.objects.get(id=user_id)

        except ChatRooms.DoesNotExist:
            return Response(
                {"error": "Chat room not found."},
                status=status.HTTP_404_NOT_FOUND,
            )
        except User.DoesNotExist:
            return Response(
                {"error": "User not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Create the message
        message = Messages.objects.create(
            chat_room=chat_room,
            user=user,
            attachment=attachment,
        )

        return Response(
            {
                "id": message.id,
                "chat_room": message.chat_room.id,
                "user": message.user.id,
                "attachment": message.attachment.url,
                "timestamp": message.timestamp,
            },
            status=status.HTTP_201_CREATED,
        )

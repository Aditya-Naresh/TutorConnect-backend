from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound
from .models import ChatRooms, Messages
from .serializers import ChatroomSerializer, MessageSerializer
import traceback
from django.utils.crypto import get_random_string

from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotAuthenticated


# Create your views here.


class MessageListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id1, user_id2):
        print("uerid", user_id1)
        print("uerid", user_id2)

        if not request.user.is_authenticated:
            raise NotAuthenticated(
                detail="User must be authenticated to view messages",
            )
        try:
            chat_room = ChatRooms.objects.filter(
                Q(user1_id=user_id1, user2_id=user_id2)
                | Q(user1_id=user_id2, user2_id=user_id1)
            ).first()  # Use .first() to get a single instance or None

            if not chat_room:
                raise NotFound("Room not found")

            messages = Messages.objects.filter(chat_room=chat_room).order_by(
                "-timestamp"
            )
            messages.filter(
                seen=False,
            ).exclude(
                user=request.user,
            ).update(
                seen=True,
            )

            serializer = MessageSerializer(messages, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except ChatRooms.DoesNotExist:
            return Response(
                {"detail": "Chat room does not exist"},
                status=status.HTTP_404_NOT_FOUND,
            )


class AddChatRoomView(APIView):
    def post(self, request):
        try:
            user_id1 = request.data.get("user_id1")
            user_id2 = request.data.get("user_id2")
            print("uesrid", user_id1)
            print("ownerrid", user_id2)

            if user_id1 == user_id2:
                return Response(
                    {"error": "Cannot create chat room with the same user."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            chat_rooms = ChatRooms.objects.filter(
                Q(user1_id=user_id1, user2_id=user_id2)
                | Q(user1_id=user_id2, user2_id=user_id1)
            )

            if chat_rooms.exists():
                chat_room = chat_rooms.first()
                serializer = ChatroomSerializer(chat_room)
                return Response(
                    serializer.data,
                    status=status.HTTP_200_OK,
                )

            else:
                chat_room = ChatRooms.objects.create(
                    user1_id=user_id1, user2_id=user_id2
                )
                serializer = ChatroomSerializer(chat_room)
                return Response(
                    serializer.data,
                    status=status.HTTP_201_CREATED,
                )

        except Exception as e:
            traceback.print_exc()
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class ListChatUsersView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        print("user: ", request.user)
        users = ChatRooms.objects.filter(
            Q(user1=request.user) | Q(user2=request.user),
        )

        if not users.exists():
            return Response(
                {"message": "No chat rooms found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = ChatroomSerializer(users, many=True)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )


class CreateMeetingView(APIView):
    def post(self, request):
        print("Request data:", request.data)
        user_id = request.data.get("userId")
        recipient_id = request.data.get("recipientId")
        print("User ID:", user_id)
        print("Recipient ID:", recipient_id)
        meeting_id = get_random_string(length=10)

        print("Generated Meeting ID:", meeting_id)
        return Response({"meetingId": meeting_id})

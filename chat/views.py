from django.db.models import Q, Count, Value
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import ChatRooms
from .serializers import ChatroomSerializer
from rest_framework.permissions import IsAuthenticated
from django.db.models.functions import Coalesce


# Create your views here.


class ListChatUsersView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        print("user: ", request.user)
        users = ChatRooms.objects.filter(
            Q(user1=request.user) | Q(user2=request.user),
        ).annotate(
            unseen_count=Coalesce(
                Count(
                    "message",
                    filter=Q(
                        message__seen=False,
                    )
                    & ~Q(
                        message__user=request.user,
                    ),
                ),
                Value(0),
            )
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

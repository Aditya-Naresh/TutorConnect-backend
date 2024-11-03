from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import (
    authentication_classes,
    permission_classes,
)


from rest_framework import permissions
from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    CreateAPIView,
    DestroyAPIView,
    UpdateAPIView,
)

from .models import Chat, Contact
from .serializers import ChatSerializer

User = get_user_model()


@api_view(["GET"])
def sample_view(request):
    data = ["foo", "bar", "baz"]
    return Response(data)


@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def protected_endpoint(request):
    return Response({"protected": "data"})


class ChatListView(ListAPIView):
    # queryset= Chat.objects.all()
    serializer_class = ChatSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        contact = get_object_or_404(Contact, user=user)
        queryset = Chat.objects.filter(participants=contact)
        email = self.request.query_params.get("email", None)

        if email is not None:
            user = get_object_or_404(User, email=email)
            contact = get_object_or_404(Contact, user=user)
            print("queryset_contact", contact)
            queryset = Chat.objects.filter(participants=contact)

        return queryset


class ChatDetailView(RetrieveAPIView):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    permission_classes = [
        permissions.AllowAny,
    ]


class ChatCreateView(CreateAPIView):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    permission_classes = [
        permissions.IsAuthenticated,
    ]


class ChatUpdateView(UpdateAPIView):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    permission_classes = [
        permissions.IsAuthenticated,
    ]


class ChatDeleteView(DestroyAPIView):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    permission_classes = [
        permissions.IsAuthenticated,
    ]

from rest_framework import serializers
from django.contrib.auth import get_user_model
from .utils import get_user_contact
from .models import Chat
from rest_framework import status
from rest_framework.exceptions import ValidationError

User = get_user_model()


class ContactSerializer(serializers.StringRelatedField):
    def to_representation(self, value):
        return f"{value.user.first_name} {value.user.last_name}"

    def to_internal_value(self, value):
        return value


class ChatSerializer(serializers.ModelSerializer):
    participants = ContactSerializer(many=True)

    class Meta:
        model = Chat
        fields = ("id", "messages", "participants")

    def create(self, validated_data):

        participants = validated_data.pop("participants")
        contacts = []
        for email in participants:
            contact = get_user_contact(email)
            contacts.append(contact)
            # chat.participants.add(contact)

        # participant1= participants[0]
        # participant2= participants[1]
        # user1= get_object_or_404(User, email=participant1)
        # user2= get_object_or_404(User, email=participant2)

        # contact1= get_object_or_404(Contact, user=user1)
        # contact2= get_object_or_404(Contact, user=user2)

        # # participants2= [participants1[1], participants1[0]]
        # print(contact1)
        # print(contact2)
        if participants[0] == participants[1]:
            raise ValidationError(
                {"error": "No place for loners :("},
                code=status.HTTP_406_NOT_ACCEPTABLE,
            )

        chat = Chat.objects.filter(participants=contacts[0]) & Chat.objects.filter(
            participants=contacts[1]
        )
        chat = chat.first()

        if chat is not None:
            return chat

        chat = Chat.objects.create()
        for email in participants:
            contact = get_user_contact(email)
            chat.participants.add(contact)

        chat.save()
        return chat


# from chat.models import Chat
# from chat.serializers import ChatSerializer
# chat= Chat.objects.get(id=3)
# s= ChatSerializer(instance=chat)
# s

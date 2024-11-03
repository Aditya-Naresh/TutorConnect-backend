from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from .models import Chat, Contact
from django.db import models

User = get_user_model()


def get_object_or_create(model: models.Model, **kwargs):
    try:
        obj = model.objects.get(**kwargs)
    except model.DoesNotExist:
        obj = model.objects.create(**kwargs)
    return obj


def previous_messages(chatId):
    chat = get_object_or_404(Chat, id=chatId)
    return chat.messages.order_by("timestamp").all()


def get_user_contact(email):
    user = get_object_or_404(User, email=email)
    contact = get_object_or_create(Contact, user=user)
    return contact


def get_current_chat(chatId):
    return get_object_or_404(Chat, id=chatId)

from django.urls import path
from .views import (
    ListChatUsersView,
)

urlpatterns = [
    path(
        "chat_users/",
        ListChatUsersView.as_view(),
        name="chat_users",
    ),
]

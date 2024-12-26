from django.urls import path
from .views import AttachmentMessageView

urlpatterns = [
    path("attachments/", AttachmentMessageView.as_view()),
]

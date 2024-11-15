from rest_framework import generics
from .permissions import IsNotificationUser
from .serializers import NotificationSerializer
from .models import Notification


class UpdateNotificationView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsNotificationUser]
    serializer_class = NotificationSerializer
    lookup_field = 'id'

    def get_queryset(self):
        user = self.request.user
        notifications = Notification.objects.filter(user=user)
        return notifications

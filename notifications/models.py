from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Notification(models.Model):
    class Types(models.TextChoices):
        BOOKING = ("BOOKING", "Booking Notification")
        UPDATE = ("UPDATE", "Update Notification")
        CANCELLATION = ("CANCELLATION", "Cancellation Notification")
        ALERT = ("ALERT", "Alert Notification")
        REPORT = ("REPORT", "Report Notification")

    type = models.CharField(
        max_length=50,
        choices=Types.choices,
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="notifications"
    )
    message = models.CharField(max_length=500)
    is_read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (
            f"{self.get_type_display()} for {self.user.get_full_name()}: {self.message}"
        )

    def mark_as_read(self):
        """Marks the notification as read."""
        self.is_read = True
        self.save()

    @classmethod
    def get_unread_for_user(cls, user):
        """Retrieve unread notifications for a specific user."""
        return cls.objects.filter(user=user, is_read=False)

    class Meta:
        ordering = ["-timestamp"]

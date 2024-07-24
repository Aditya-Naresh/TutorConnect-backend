from django.db import models
from accounts.models import *
from datetime import timedelta
from django.core.exceptions import ValidationError

# Create your models here.


class TimeSlots(models.Model):
    class Meta:
        verbose_name = 'Time Slot'
        verbose_name_plural = 'Time Slots'

    class Status(models.TextChoices):
        AVAILABLE = 'AVAILABLE', 'Available'
        BOOKED = 'BOOKED', 'Booked'
        COMPLETED = 'COMPLETED', 'Completed'
        CANCELLED = 'CANCELLED', 'Cancelled'

    start_time = models.DateTimeField()
    end_time = models.DateTimeField(blank=True, null=True)
    subject = models.ForeignKey(
        Subject, on_delete=models.CASCADE, null=True, blank=True)
    status = models.CharField(
        max_length=100, choices=Status.choices, default=Status.AVAILABLE)
    tutor = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name=('tutor_slots'))
    student = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True, related_name=('student_slots'))
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def clean(self) -> None:
        if self.subject and self.subject.owner != self.tutor:
            raise ValidationError("Only the Tutor's Subjects are allowed")

        if self.tutor.role != User.Role.TUTOR:
            raise ValidationError(
                "Only the Tutors are allowed to be in Tutor Field")

        if self.student and self.student.role != User.Role.STUDENT:
            raise ValidationError(
                "Only Students are allowed to book the time slots")

    def save(self, *args, **kwargs):
        self.clean()

        if self.start_time:
            self.end_time = self.start_time + timedelta(hours=1)
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.tutor.first_name} : {self.start_time}"

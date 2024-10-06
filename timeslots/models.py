from django.db import models
from accounts.models import User, Subject
from datetime import timedelta
from django.core.exceptions import ValidationError

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
            raise ValidationError("Only the Tutors are allowed to be in Tutor Field")

        if self.student and self.student.role != User.Role.STUDENT:
            raise ValidationError("Only Students are allowed to book the time slots")

        if self.start_time and self.end_time:
            overlapping_slots = TimeSlots.objects.filter(
                tutor=self.tutor,
                start_time__lt=self.end_time,
                end_time__gt=self.start_time
            ).exclude(id=self.id)  

            if overlapping_slots.exists():
                print(overlapping_slots)
                raise ValidationError("This time slot overlaps with an existing slot.")
            

    def save(self, *args, **kwargs):
        self.clean()

        # Automatically set end_time if not provided
        if self.start_time:
            self.end_time = self.start_time + timedelta(hours=1)

        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.tutor.first_name} : {self.start_time}"

class TuitionRequest(models.Model):
    student = models.ForeignKey(User, related_name="tuition_requests_as_student", blank=True, null=True, on_delete=models.CASCADE)
    tutor = models.ForeignKey(User, related_name="tuition_requests_as_tutor", on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, related_name="tuition_request_subject", on_delete=models.CASCADE)
    is_accepted = models.BooleanField(default=False)
    tutor_viewed = models.BooleanField(default=False)
    student_viewed = models.BooleanField(default=False)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"TuitionRequest from {self.student.first_name} to {self.tutor.first_name}"

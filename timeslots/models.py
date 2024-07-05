from django.db import models
from accounts.models import User, Subject
from django.core.exceptions import ValidationError
from django.utils.text import slugify
from datetime import timedelta, datetime



# Create your models here.

class TutorDates(models.Model):
    date = models.DateField()
    tutor = models.ForeignKey(User, on_delete=models.CASCADE)
    slug = models.SlugField(unique=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.tutor.role != User.Role.TUTOR:
            raise ValidationError("The selected user must have the role of TUTOR.")
        
        self.slug = slugify(f"{self.tutor.first_name}-{self.date}")
        
        if TutorDates.objects.filter(tutor=self.tutor, date=self.date).exists():
            raise ValidationError("This date is already taken for this tutor.")
        
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.tutor.first_name} on {self.date}"
    

class TimeSlots(models.Model):
    start_time = models.TimeField()
    end_time = models.TimeField(blank=True)
    date = models.ForeignKey(TutorDates, on_delete=models.CASCADE)
    is_booked = models.BooleanField(default=False)
    booked_by = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, default=None)

    def save(self, *args, **kwargs):
        if not self.end_time:
            start_datetime = datetime.combine(datetime.today(), self.start_time)
            self.end_time = (start_datetime + timedelta(hours=1)).time()

        if not self.pk:
            overlapping_slots = TimeSlots.objects.filter(
                date=self.date,
                start_time__lt=self.end_time,
                end_time__gt=self.start_time
            )

            if overlapping_slots.exists():
                raise ValidationError("Time slot overlaps with an existing slot.")

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.start_time} - {self.end_time} on {self.date}" 
    





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

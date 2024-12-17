from rest_framework import serializers
from timeslots.models import TimeSlots


class TimeSlotSerializer(serializers.ModelSerializer):
    tutor_email = serializers.SerializerMethodField()
    student_email = serializers.SerializerMethodField()

    class Meta:
        model = TimeSlots
        fields = [
            "id",
            "status",
            "tutor",
            "tutor_email",
            "student",
            "student_email",
        ]

    def get_tutor_email(self, obj):
        return obj.tutor.email

    def get_student_email(self, obj):
        return obj.student.email

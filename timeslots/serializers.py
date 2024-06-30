from rest_framework import serializers
from .models import TutorDates, TimeSlots

class TutdorDateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TutorDates
        fields = "__all__"


class TimeSlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeSlots
        fields = "__all__"
        read_only_fields = ['end_time', 'date', 'is_booked', 'booked_by']
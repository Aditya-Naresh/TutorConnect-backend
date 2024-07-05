from rest_framework import serializers
from .models import TutorDates, TimeSlots, TuitionRequest
from accounts.models import User, Subject

class TutdorDateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TutorDates
        fields = "__all__"


class CreateTimeSlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeSlots
        fields = "__all__"
        read_only_fields = ['end_time', 'date', 'is_booked', 'booked_by']

class TimeSlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeSlots
        fields = "__all__"

    def validate(self, attrs):
        instance = self.instance  
        start_time = attrs.get('start_time', instance.start_time if instance else None)
        end_time = attrs.get('end_time', instance.end_time if instance else None)
        date = attrs.get('date', instance.date if instance else None)

        if date:
            overlapping_slots = TimeSlots.objects.filter(
                date=date,
                start_time__lt=end_time,
                end_time__gt=start_time
            ).exclude(pk=instance.pk if instance else None)

            if overlapping_slots.exists():
                raise serializers.ValidationError("Time slot overlaps with an existing slot.")

        return attrs

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['id','name']

class TutorSerializer(serializers.ModelSerializer):
    subjects = SubjectSerializer(many=True, read_only=True)
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'subjects', 'rate']



class TuitionRequestSerializer(serializers.ModelSerializer):
    tutor_name = serializers.SerializerMethodField()
    student_name = serializers.SerializerMethodField()
    subject_name = serializers.SerializerMethodField()

    class Meta:
        model = TuitionRequest
        fields = '__all__'
        read_only_fields = ['id', 'created_at']

    def get_tutor_name(self, obj):
        return f"{obj.tutor.first_name} {obj.tutor.last_name}"

    def get_student_name(self, obj):
        return f"{obj.student.first_name} {obj.student.last_name}"
    
    def get_subject_name(self, obj):
        return obj.subject.name if obj.subject else None
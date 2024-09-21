from rest_framework import serializers
from django.utils.timezone import now
from .models import *

class TimeSlotSerializer(serializers.ModelSerializer):
    title = serializers.CharField(source='status')
    start = serializers.DateTimeField(source='start_time')
    end = serializers.DateTimeField(source='end_time', read_only=True)
    className = serializers.CharField(source='status')
    student_name = serializers.SerializerMethodField()
    tutor_name = serializers.SerializerMethodField()
    subject_name = serializers.SerializerMethodField()
    rate = serializers.SerializerMethodField()

    class Meta:
        model = TimeSlots
        fields = ['id', 'start', 'end', 'subject', 'tutor', 'student','title', 'className', "student_name", "tutor_name", "rate", "subject_name"]

    def validate(self, data):
        start_time = self.instance.start_time if self.instance else data.get('start_time')
        tutor = self.instance.tutor if self.instance else data.get('tutor')
        slot_id = self.instance.id if self.instance else None


        if start_time is None:
            raise serializers.ValidationError({
                'start': 'Start time is required.'
            })

        # Calculate the potential end_time (assuming 1-hour duration)
        try:
            end_time = start_time + timedelta(hours=1)
        except TypeError:
            raise serializers.ValidationError({
                'start': 'Invalid start time format.'
            })

        # Check for overlapping time slots
        overlapping_slots = TimeSlots.objects.filter(
            tutor=tutor,
            start_time__lt=end_time,
            end_time__gt=start_time
        ).exclude(id=slot_id)

        if overlapping_slots.exists():
            raise serializers.ValidationError("This time slot overlaps with an existing slot.")

        return data

    def get_student_name(self, obj):
        return obj.student.get_full_name() if obj.student else ""
    
    def get_tutor_name(self, obj):
        return obj.tutor.get_full_name() if obj.tutor else ""
    
    def get_subject_name(self, obj):
        return obj.subject.name if obj.subject else ""
    
    def get_rate(self, obj):
        return obj.tutor.rate



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
    



class CreateTimeSlotsSerializer(serializers.Serializer):
    start_time = serializers.DateTimeField()
    end_time = serializers.DateTimeField()

    def validate(self, attrs):
        start_time = attrs['start_time']
        end_time = attrs['end_time']

        if start_time >= end_time:
            raise serializers.ValidationError("End time must be after start time.")
        
        if start_time < now():
            raise serializers.ValidationError("Start time cannot create time slot in the past")
        return attrs
    

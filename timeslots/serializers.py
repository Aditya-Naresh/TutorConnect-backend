from rest_framework import serializers
from .models import *

class TimeSlotSerializer(serializers.ModelSerializer):
    title = serializers.CharField(source='status')
    start = serializers.DateTimeField(source='start_time')
    end = serializers.DateTimeField(source='end_time', allow_null = True)
    className = serializers.CharField(source='status')
    student_name = serializers.SerializerMethodField()
    tutor_name = serializers.SerializerMethodField()
    subject = serializers.SerializerMethodField()
    rate = serializers.SerializerMethodField()

    class Meta:
        model = TimeSlots
        fields = ['id', 'start', 'end', 'subject', 'tutor', 'student','title', 'className', "student_name", "tutor_name", "rate"]

    def get_student_name(self, obj):
        if obj.student:
            name =  obj.student.get_full_name()
        else:
            name = ""
        return name
    
    def get_tutor_name(self, obj):
        if obj.tutor:
            name =  obj.tutor.get_full_name()
        else:
            name = ""
        return name
    
    def get_subject(self, obj):
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
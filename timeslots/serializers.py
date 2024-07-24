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

    class Meta:
        model = TimeSlots
        fields = ['id', 'start', 'end', 'subject', 'tutor', 'student','title', 'className', "student_name", "tutor_name"]

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
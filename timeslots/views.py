from rest_framework import generics
from .serializers import *
from rest_framework.response import Response
from .models import *
from .permissions import *
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q

class TutorTimeSlotView(generics.ListCreateAPIView):
    permission_classes = [TutorPermission]
    serializer_class = TimeSlotSerializer

    def get_queryset(self):
        return TimeSlots.objects.filter(tutor=self.request.user)


class RetrieveUpdateTimeSlotView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TimeSlotSerializer
    queryset = TimeSlots.objects.all()
    lookup_field = 'id'


class StudentTimeSlotView(generics.ListAPIView):
    permission_classes = [StudentPermission]
    serializer_class = TimeSlotSerializer

    def get_queryset(self):
        return TimeSlots.objects.filter(student=self.request.user)
    

class TutorListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TutorSerializer


    def get_queryset(self):
        queryset = Tutor.objects.filter(is_approved = True)
        keyword = self.request.query_params.get('keyword')
        if keyword:
            queryset = queryset.filter(
                Q(first_name__icontains = keyword) |
                Q(last_name__icontains = keyword) |
                Q(subjects__name__icontains=keyword)
            ).distinct()
        return queryset

    

class TuitionRequestListCreateView(generics.ListCreateAPIView):
    serializer_class = TuitionRequestSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'TUTOR':
            return TuitionRequest.objects.filter(tutor_viewed=False, tutor=user)
        elif user.role == 'STUDENT':
            return TuitionRequest.objects.filter(tutor_viewed=True, student_viewed=False, student=user)
        else:
            return TuitionRequest.objects.none() 


class TuitionRequestRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    serializer_class = TuitionRequestSerializer
    permission_classes = [IsAuthenticated]
    lookup_field ='id'

    def get_queryset(self):
        user = self.request.user
        if user.role == 'TUTOR':
            return TuitionRequest.objects.filter(tutor_viewed=False, tutor=user)
        elif user.role == 'STUDENT':
            return TuitionRequest.objects.filter(tutor_viewed=True, student_viewed=False, student=user)
        else:
            return TuitionRequest.objects.none() 
        


class TutorTimeSlotsListView(generics.ListAPIView):
    serializer_class = TimeSlotSerializer
    permission_classes = [StudentPermission]
    

    def get_queryset(self):
        tutor_id = self.kwargs['tutor_id']
        return TimeSlots.objects.filter(tutor__id = tutor_id)
    
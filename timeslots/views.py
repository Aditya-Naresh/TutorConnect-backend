from datetime import timedelta
from django.utils.dateparse import parse_date
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import TutorDates, TimeSlots, TuitionRequest
from accounts.models import User, Tutor
from .serializers import TutdorDateSerializer, TimeSlotSerializer, TutorSerializer, TuitionRequestSerializer,CreateTimeSlotSerializer
from django.shortcuts import get_object_or_404
from django.db.models import Q
from rest_framework.exceptions import ValidationError


class CreateTutorDatesView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        start_date = parse_date(request.data.get('start_date'))
        end_date = parse_date(request.data.get('end_date'))

        if not start_date or not end_date:
            return Response(
                {"message": "Start date and end date are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if request.user.role != User.Role.TUTOR:
            return Response(
                {"messaage": "You must be a tutor to create dates."},
                status=status.HTTP_403_FORBIDDEN
            )

        current_date = start_date
        while current_date <= end_date:
            TutorDates.objects.create(date=current_date, tutor=request.user)
            current_date += timedelta(days=1)

        return Response({"message": "Tutor dates created successfully."}, status=status.HTTP_201_CREATED)





class TutorDatesListView(generics.ListAPIView):
    serializer_class = TutdorDateSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user_id = self.kwargs['id']
        user = get_object_or_404(User, id=user_id)
        return TutorDates.objects.filter(tutor=user)
    


class TimeSlotsListView(generics.ListCreateAPIView):
    serializer_class = CreateTimeSlotSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        date_id = self.kwargs['id']
        date = get_object_or_404(TutorDates, id=date_id)
        return TimeSlots.objects.filter(date=date)

    def create(self, request, *args, **kwargs):
        date_id = self.kwargs['id']
        date = get_object_or_404(TutorDates, id=date_id)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(date=date)  
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    


class TimeSlotRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    serializer_class = TimeSlotSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'
    queryset = TimeSlots.objects.all()


    def patch(self, request, *args, **kwargs):
        try:
            return super().patch(request, *args, **kwargs)
        except ValidationError as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)


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
            return TuitionRequest.objects.none()  # Handle other roles or unauthenticated users

class TuitionRequestRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    serializer_class = TuitionRequestSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'

    def get_queryset(self):
        user = self.request.user
        if user.role == 'TUTOR':
            return TuitionRequest.objects.filter(tutor=user)
        elif user.role == 'STUDENT':
            return TuitionRequest.objects.filter(student=user)
        else:
            return TuitionRequest.objects.none()  


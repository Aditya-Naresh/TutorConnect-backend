from rest_framework import generics, status
from .serializers import (
    TimeSlotSerializer,
    CreateTimeSlotsSerializer,
    TutorSerializer,
)
from rest_framework.response import Response
from .models import TimeSlots
from .permissions import TutorPermission, StudentPermission
from accounts.models import Tutor
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from datetime import timedelta


class TutorTimeSlotView(generics.ListCreateAPIView):
    permission_classes = [TutorPermission]
    serializer_class = TimeSlotSerializer

    def get_queryset(self):
        return TimeSlots.objects.filter(tutor=self.request.user)


class StudentRetrieveUpdateTimeSlotView(generics.RetrieveUpdateAPIView):
    permission_classes = [StudentPermission]
    serializer_class = TimeSlotSerializer
    queryset = TimeSlots.objects.filter(
        tutor__is_blocked=False, status=TimeSlots.Status.AVAILABLE
    )
    lookup_field = "id"


class RetrieveUpdateTimeSlotView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TimeSlotSerializer
    queryset = TimeSlots.objects.all()
    lookup_field = "id"


class StudentTimeSlotView(generics.ListAPIView):
    permission_classes = [StudentPermission]
    serializer_class = TimeSlotSerializer

    def get_queryset(self):
        return TimeSlots.objects.filter(student=self.request.user)


class TutorListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TutorSerializer
    lookup_field = "id"

    def get_queryset(self):
        queryset = Tutor.objects.filter(is_approved=True, is_blocked=False)
        tutor_id = self.kwargs.get("id") or self.request.query_params.get("id")
        if tutor_id:
            return Tutor.objects.filter(id=tutor_id, is_approved=True)

        keyword = self.request.query_params.get("keyword")
        if keyword:
            queryset = queryset.filter(
                Q(first_name__icontains=keyword)
                | Q(last_name__icontains=keyword)
                | Q(subjects__name__icontains=keyword)
            ).distinct()
        return queryset


class TutorTimeSlotsListView(generics.ListAPIView):
    serializer_class = TimeSlotSerializer
    permission_classes = [StudentPermission]

    def get_queryset(self):
        tutor_id = self.kwargs["tutor_id"]
        return TimeSlots.objects.filter(
            tutor__id=tutor_id, status=TimeSlots.Status.AVAILABLE
        )


class CreateTimeSlotsView(generics.GenericAPIView):
    permission_classes = [TutorPermission]
    serializer_class = CreateTimeSlotsSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        start_time = serializer.validated_data["start_time"]
        end_time = serializer.validated_data["end_time"]
        tutor = request.user

        created_slots = []
        current_time = start_time

        while current_time < end_time:
            slot_end_time = current_time + timedelta(hours=1)

            if not TimeSlots.objects.filter(
                tutor=tutor,
                start_time__lt=slot_end_time,
                end_time__gt=current_time,
            ).exists():
                slot = TimeSlots.objects.create(
                    tutor=tutor,
                    start_time=current_time,
                    end_time=slot_end_time,
                    status=TimeSlots.Status.AVAILABLE,
                )
                created_slots.append(slot)

            current_time = slot_end_time

        if not created_slots:
            return Response(
                {"message": "All potential slots overlap with existing ones"},
                status=status.HTTP_200_OK,
            )
        message = f"{len(created_slots)} time slots created successfully"
        return Response(
            {"message": message},
            status=status.HTTP_201_CREATED,
        )


class TimeSlotHistoryView(generics.ListAPIView):
    serializer_class = TimeSlotSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user_id = self.kwargs["id"]
        queryset = TimeSlots.objects.filter(
            id=user_id,
            status=TimeSlots.Status.COMPLETED,
        )

        return queryset

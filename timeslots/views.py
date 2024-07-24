from rest_framework import generics
from .serializers import *
from rest_framework.response import Response
from .models import *
from .permissions import *
from rest_framework.permissions import IsAuthenticated

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
from rest_framework import generics
from accounts.models import Tutor, Student, User, Subject, Certification
from timeslots.models import TimeSlots
from .serializers import (
    UserSerializer,
    SubjectSerializer,
    CertificationSerializer,
    TimeSlotSerializer,
    WalletTransactionSerializer,
)
from wallets.models import WalletTransaction
from .permissions import IsAdminUser

# Create your views here.


class TutorListView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        path = self.request.path_info

        if "/approval/" in path:
            return Tutor.objects.filter(
                is_approved=False,
                is_submitted=True,
            )
        else:
            return Tutor.objects.all()


class StudentListView(generics.ListAPIView):
    queryset = Student.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]


class UserUpdateView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = "id"
    permission_classes = [IsAdminUser]


class SubjectListView(generics.ListAPIView):
    serializer_class = SubjectSerializer
    permission_classes = [IsAdminUser]
    serializer_class = WalletTransactionSerializer
    queryset = WalletTransaction.objects.all()

    def get_queryset(self):
        user = User.objects.get(pk=self.kwargs.get("user_id"))
        return Subject.objects.filter(owner=user)


class CertificationListView(generics.ListAPIView):
    serializer_class = CertificationSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        user = User.objects.get(pk=self.kwargs.get("user_id"))
        return Certification.objects.filter(owner=user)


class CancelledTimeSlotListView(generics.ListAPIView):
    serializer_class = TimeSlotSerializer
    permission_classes = [IsAdminUser]
    queryset = TimeSlots.objects.filter(status=TimeSlots.Status.CANCELLED)


class UpdateTimeSlotView(generics.RetrieveUpdateAPIView):
    serializer_class = TimeSlotSerializer
    permission_classes = [IsAdminUser]
    lookup_field = "id"
    queryset = TimeSlots.objects.all()


class RefundView(generics.CreateAPIView):
    serializer_class = WalletTransactionSerializer
    queryset = WalletTransaction.objects.all()
    permission_classes = [IsAdminUser]

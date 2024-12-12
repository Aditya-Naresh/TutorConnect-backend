from rest_framework import serializers
from accounts.models import User, Subject, Certification
from timeslots.models import TimeSlots
from wallets.models import Wallet, WalletTransaction


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "email",
            "id",
            "is_blocked",
            "is_active",
            "auth_provider",
            "is_approved",
            "rate",
            "is_submitted",
        ]


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = "__all__"


class CertificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certification
        fields = "__all__"


class TimeSlotSerializer(serializers.ModelSerializer):
    subject_name = serializers.SerializerMethodField()
    tutor_name = serializers.SerializerMethodField()
    student_name = serializers.SerializerMethodField()
    cancelled_by = serializers.SerializerMethodField()
    student_wallet = serializers.SerializerMethodField()

    class Meta:
        model = TimeSlots
        fields = [
            "id",
            "start_time",
            "end_time",
            "status",
            "rate",
            "subject",
            "subject_name",
            "tutor",
            "tutor_name",
            "student",
            "student_name",
            "cancelled_by",
            "student_wallet",
        ]

    def get_subject_name(self, obj):
        return obj.subject.name

    def get_tutor_name(self, obj):
        return obj.tutor.get_full_name() if obj.tutor else ""

    def get_student_name(self, obj):
        return obj.student.get_full_name() if obj.student else ""

    def get_cancelled_by(self, obj):
        if obj.student == obj.cancelled_by:
            return "STUDENT"
        elif obj.tutor == obj.cancelled_by:
            return "TUTOR"

    def get_student_wallet(self, obj):
        return Wallet.objects.get(owner=obj.student).pk


class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = "__all__"


class WalletTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = WalletTransaction
        fields = "__all__"

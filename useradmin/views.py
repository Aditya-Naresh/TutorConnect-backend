from django.shortcuts import render
from rest_framework import generics
from accounts.models import Tutor, Student, User
from . serializers import UserSerializer
from . permissions import IsAdminUser
# Create your views here.

class TutorListView(generics.ListAPIView):
    queryset = Tutor.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]

class StudentListView(generics.ListAPIView):
    queryset = Student.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]

class UserUpdateView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'id'
    permission_classes = [IsAdminUser]
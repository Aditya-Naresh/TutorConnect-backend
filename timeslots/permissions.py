from rest_framework.permissions import BasePermission
from . models import User



class TutorPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == User.Role.TUTOR
    


class StudentPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == User.Role.STUDENT
    
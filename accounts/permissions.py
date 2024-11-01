from rest_framework.permissions import BasePermission
from .models import User


class IsOwnerTutorOnly(BasePermission):
    def has_permission(self, request, view):
        authenticated = request.user.is_authenticated
        role_match = request.user.role == User.Role.TUTOR
        return authenticated and role_match

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user

from rest_framework.permissions import BasePermission
from . models import User


class IsOwnerTutorOnly(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == User.Role.TUTOR
    
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user
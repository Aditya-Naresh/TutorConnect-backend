from rest_framework.permissions import BasePermission
from accounts.models import User


class IsAdminUser(BasePermission):
    def has_permission(self, request, view):
        is_admin = request.user.role == User.Role.ADMIN
        return request.user.is_authenticated and is_admin

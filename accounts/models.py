from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from .managers import UserManager, ProxyManager
from rest_framework_simplejwt.tokens import RefreshToken
# Create your models here.
AUTH_PROVIDERS = {
    'email': 'email',
    'google': 'google'
}


class User(AbstractBaseUser, PermissionsMixin):
    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        STUDENT = "STUDENT", "Student"
        TUTOR = "TUTOR", "Tutor"
    base_role = Role.ADMIN
    role = models.CharField(
        max_length=50, choices=Role.choices, default=base_role)
    email = models.EmailField(
        max_length=255, unique=True, verbose_name=_("Email Address"))
    first_name = models.CharField(max_length=100, verbose_name=_("First Name"))
    last_name = models.CharField(max_length=100, verbose_name=_("Last Name"))
    # Add other fields in the project

    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_blocked = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    auth_provider = models.CharField(
        max_length=50, default=AUTH_PROVIDERS.get("email"))

    USERNAME_FIELD = "email"

    REQUIRED_FIELDS = ["first_name", "last_name"]

    objects = UserManager()

    def __str__(self) -> str:
        return self.email

    @property
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }


class Student(User):
    base_role = User.Role.STUDENT
    objects = ProxyManager()
    class Meta:
        proxy = True


class Tutor(User):
    base_role = User.Role.TUTOR
    objects = ProxyManager()
    class Meta:
        proxy = True

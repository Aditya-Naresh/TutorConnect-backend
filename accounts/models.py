from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from .managers import UserManager, ProxyManager
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.validators import FileExtensionValidator
from django.utils.text import slugify
from phonenumber_field.modelfields import PhoneNumberField
import os

# Create your models here.


class User(AbstractBaseUser, PermissionsMixin):
    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        STUDENT = "STUDENT", "Student"
        TUTOR = "TUTOR", "Tutor"
        NEW = "NEW", "New"

    class AuthProviders(models.TextChoices):
        EMAIL = "EMAIL", "Email"
        GOOGLE = "GOOGLE", "Google"

    base_role = Role.ADMIN
    role = models.CharField(
        max_length=50,
        choices=Role.choices,
        default=base_role,
    )
    email = models.EmailField(
        max_length=255, unique=True, verbose_name=_("Email Address")
    )
    first_name = models.CharField(max_length=100, verbose_name=_("First Name"))
    last_name = models.CharField(max_length=100, verbose_name=_("Last Name"))
    profile_pic = models.ImageField(
        upload_to="profile_pictures/",
        null=True,
        blank=True,
        validators=[FileExtensionValidator(["jpg", "jpeg", "png"])],
    )
    phone_number = PhoneNumberField(
        null=True,
        unique=True,
        default=None,
        verbose_name=_("Phone Number"),
    )
    # Only used in TutorProfiles
    is_submitted = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)
    rate = models.DecimalField(default=100, max_digits=6, decimal_places=2)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_blocked = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    auth_provider = models.CharField(
        max_length=50,
        choices=AuthProviders.choices,
        default=AuthProviders.EMAIL,
    )

    USERNAME_FIELD = "email"

    REQUIRED_FIELDS = ["first_name", "last_name"]

    objects = UserManager()

    def __str__(self) -> str:
        return f"{self.pk} : {self.email}"

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def tokens(self):
        try:
            refresh = RefreshToken.for_user(self)
            return {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }
        except Exception as e:
            print("Tokens Error:", e)

    def save(self, *args, **kwargs):
        if self.pk:
            old_image = User.objects.get(pk=self.pk).profile_pic
            if old_image and old_image != self.profile_pic:
                if os.path.isfile(old_image.path):
                    os.remove(old_image.path)
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.profile_pic:
            if os.path.isfile(self.profile_pic.pah):
                os.remove(self.profile_pic.path)
        super().delete(*args, **kwargs)


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


# Subjects and Certifications of Tutors


class Subject(models.Model):
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(
        User,
        related_name="subjects",
        on_delete=models.CASCADE,
        limit_choices_to={"role": User.Role.TUTOR},
    )
    slug = models.SlugField(max_length=150, unique=True, blank=True, null=True)

    class Meta:
        unique_together = ("owner", "slug")

    def save(self, *args, **kwargs):
        if self.owner.role != User.Role.TUTOR:
            raise ValueError("Only tutors can be assigned subjects")
        if not self.slug:
            self.slug = slugify(f"{self.owner.id}-{self.name}")

        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name


class Certification(models.Model):
    title = models.CharField(max_length=100)
    file = models.FileField(
        upload_to="certifications/",
        validators=[FileExtensionValidator(["pdf"])],
    )
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={"role": User.Role.TUTOR},
    )
    slug = models.SlugField(max_length=150, unique=True, blank=True, null=True)
    reupload = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.owner.role != User.Role.TUTOR:
            raise ValueError(
                "Only tutors are required to submit Certifications",
            )
        if not self.slug:
            self.slug = slugify(f"{self.owner.id}-{self.title}")
        if self.pk:
            old_file = Certification.objects.get(pk=self.pk).file
            if old_file and old_file != self.file:
                if os.path.isfile(old_file.path):
                    os.remove(old_file.path)
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.file:
            if os.path.isfile(self.file.path):
                os.remove(self.file.path)

        super().delete(*args, **kwargs)

    def __str__(self) -> str:
        return self.title

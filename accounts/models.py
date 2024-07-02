from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from .managers import UserManager, ProxyManager
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.validators import FileExtensionValidator
from django.utils.text import slugify




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
        #Only used in TutorProfiles 
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



# Subjects and Certifications of Tutors

class Subject(models.Model):
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(User,related_name='subjects', on_delete=models.CASCADE, limit_choices_to={'role' : User.Role.TUTOR})
    slug = models.SlugField(max_length=150, unique=True, blank=True, null=True)

    class Meta:
        unique_together = ('owner', 'slug')

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
    image = models.ImageField(upload_to='certifications/', validators=[FileExtensionValidator(['jpg', 'jpeg'])])
    owner = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': User.Role.TUTOR})
    slug = models.SlugField(max_length=150, unique=True, blank=True, null=True)
    reupload = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.owner.role != User.Role.TUTOR:
            raise ValueError("Only tutors are required to submit Certifications")
        if not self.slug:
            self.slug = slugify(f"{self.owner.id}-{self.title}")
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.title
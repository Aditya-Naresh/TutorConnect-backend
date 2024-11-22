from django.contrib.auth.models import BaseUserManager
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.db.models.query import QuerySet
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    def email_validation(self, email):
        try:
            validate_email(email)
        except ValidationError:
            raise ValidationError(_("You must provide a valid email"))

    def create_user(
        self, email, first_name, last_name=None, password=None, **extra_fields
    ):
        if not email:
            raise ValueError(_("Email is required"))
        else:
            self.email_validation(email)
            clean_email = self.normalize_email(email)

        if not first_name:
            raise ValueError(_("First Name is required"))

        user = self.model(
            email=clean_email,
            first_name=first_name,
            last_name=last_name,
            **extra_fields
        )
        user.set_password(password)
        user.role = self.model.base_role
        extra_fields.setdefault("is_superuser", False)
        extra_fields.setdefault("is_staff", False)

        user.save()
        return user

    def create_superuser(
        self, email, first_name, last_name=None, password=None, **extra_fields
    ):
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_verified", True)
        if not email:
            raise ValidationError(_("This is a required field"))
        else:
            self.email_validation(email)
            clean_email = self.normalize_email(email)

        if not first_name:
            raise ValueError(_("This is a required field"))

        if extra_fields.get("is_superuser") is not True:
            raise ValueError(
                _("Superuser must have True Value in  is_superuser field"),
            )
        if extra_fields.get("is_staff") is not True:
            raise ValueError(
                _("Superuser must have True value in is_staff field"),
            )

        user = self.create_user(
            clean_email, first_name, last_name, password, **extra_fields
        )
        user.role = self.model.base_role
        user.save()
        return user


class ProxyManager(UserManager):
    def get_queryset(self) -> QuerySet:
        return (
            super()
            .get_queryset()
            .filter(
                role=self.model.base_role,
            )
        )

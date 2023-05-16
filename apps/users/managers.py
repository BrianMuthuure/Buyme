from django.contrib.auth.models import BaseUserManager
from django.core.exceptions import ValidationError
from django.core.validators import validate_email


class CustomUserManager(BaseUserManager):

    def validate_email(self, email):
        try:
            validate_email(email)
        except ValidationError:
            raise ValueError("You must provide a valid email address")

    def create_user(self, first_name, last_name, email, password=None, **extra_fields):
        if not email:
            raise ValueError("User must have an email address")
        if not first_name:
            raise ValueError("User must have a first name")
        if not last_name:
            raise ValueError("User must have a last name")
        email = self.normalize_email(email)
        user = self.model(
            first_name=first_name,
            last_name=last_name,
            email=email,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, first_name, last_name,  email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have admin=True.")
        if not password:
            raise TypeError("Superuser must have a password.")
        user = self.create_user(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password,
            **extra_fields
        )
        user.save(using=self._db)
        return user

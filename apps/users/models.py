from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from .managers import CustomUserManager
from django.utils.translation import gettext_lazy as _


class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("First Name"))
    middle_name = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("Middle Name"))
    last_name = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("Last Name"))
    email = models.EmailField(unique=True, verbose_name=_("Email"))
    date_joined = models.DateTimeField(default=timezone.now, editable=False, verbose_name=_("Date Joined"))
    last_login = models.DateTimeField(blank=True, null=True, verbose_name=_("Last Login"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated At"))
    birth_date = models.DateField(blank=True, null=True, verbose_name=_("Date of Birth"))
    is_active = models.BooleanField(default=True, verbose_name=_("Is Active"))
    staff = models.BooleanField(default=False, verbose_name=_("Is Staff"))
    admin = models.BooleanField(default=False, verbose_name=_("Is Admin"))

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    objects = CustomUserManager()

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")
        db_table = "users"

    def clean(self):
        super().clean()
        if self.birth_date and self.birth_date > timezone.now().date():
            raise ValidationError(_("Birth date cannot be in the future."))
        if self.birth_date and self.birth_date > timezone.now().date() - timezone.timedelta(days=365 * 18):
            raise ValidationError(_("You must be at least 18 years old to register."))
        if self.birth_date and self.birth_date < timezone.now().date() - timezone.timedelta(days=365 * 120):
            raise ValidationError(_("You must be at most 120 years old to register."))

    def __str__(self):
        return self.email

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def get_short_name(self):
        return self.first_name

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def age(self):
        today = timezone.now().date()
        age = int(
            today.year
            -
            (self.birth_date.year)
            -
            ((today.month, today.day) < (self.birth_date.month, self.birth_date.day))
        )
        return age

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin

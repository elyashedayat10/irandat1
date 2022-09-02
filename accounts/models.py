from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models

from .managers import UserManager
from django.utils import timezone


# Create your models here.


class User(AbstractBaseUser, PermissionsMixin):
    phone_number = models.CharField(max_length=11, unique=True)
    first_name = models.CharField(max_length=125)
    last_name = models.CharField(max_length=125)
    email = models.CharField(max_length=125, null=True, blank=True)
    joined = models.DateTimeField(auto_now_add=True)
    promoted_date = models.DateTimeField(blank=True, null=True)
    description = models.TextField(blank=True)

    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = ["first_name", "last_name", "email"]

    objects = UserManager()

    def __str__(self):
        return self.phone_number

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin


class OtpCode(models.Model):
    phone_number = models.CharField(max_length=11)
    code = models.CharField(max_length=6)
    created = models.DateTimeField(auto_now_add=True)

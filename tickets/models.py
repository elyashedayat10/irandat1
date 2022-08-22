import random

from django.conf import settings
from django.db import models

user = settings.AUTH_USER_MODEL


def create_new_ref_number():
    return str(random.randint(1000000000, 9999999999))


# Create your models here.


class Ticket(models.Model):
    class TYPE(models.TextChoices):
        Technical = "فنی", "فنی"  # Technical
        financial = "مالی", "مالی"  # Financial
        support = "پشتیبانی", "پشتیبانی"  # Support

    class Status(models.TextChoices):
        waiting = "در انتظار پاسخ", "در انتظار پاسخ"  # Waiting
        answered = "پاسخ داده شده", "پاسخ داده شده"  # Answeres
        closed = "بسته شده", "بسته شده"  # Closed

    user = models.ForeignKey(user, on_delete=models.CASCADE, related_name="tickets")
    title = models.CharField(max_length=255)
    type = models.CharField(max_length=20, choices=TYPE.choices)
    status = models.CharField(
        max_length=20, choices=Status.choices, default="در انتظار پاسخ"
    )
    closed_at = models.DateTimeField(null=True, blank=True)
    code = models.CharField(max_length=124, unique=True, default=create_new_ref_number)
    created = models.DateTimeField(auto_now_add=True)


class Answer(models.Model):
    class WHO_CHOICES(models.TextChoices):
        admin = "admin", "ادمین"  # َََAdmin
        user = "user", "کاربر"  # User

    from_who = models.CharField(max_length=20, choices=WHO_CHOICES.choices)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name="answers")
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

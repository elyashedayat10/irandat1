# Generated by Django 4.0.6 on 2022-08-01 19:45

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models

import tickets.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Ticket",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=255)),
                (
                    "type",
                    models.CharField(
                        choices=[
                            ("فنی", "فنی"),
                            ("مالی", "مالی"),
                            ("پشتیبانی", "پشتیبانی"),
                        ],
                        max_length=20,
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("در انتظار پاسخ", "در انتظار پاسخ"),
                            ("پاسخ داده شده", "پاسخ داده شده"),
                            ("بسته شده", "بسته شده"),
                        ],
                        default="در انتظار پاسخ",
                        max_length=20,
                    ),
                ),
                ("closed_at", models.DateTimeField(blank=True, null=True)),
                (
                    "code",
                    models.CharField(
                        default=tickets.models.create_new_ref_number,
                        max_length=124,
                        unique=True,
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="tickets",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Answer",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "from_who",
                    models.CharField(
                        choices=[("admin", "ادمین"), ("user", "کاربر")], max_length=20
                    ),
                ),
                ("body", models.TextField()),
                ("created", models.DateTimeField(auto_now_add=True)),
                (
                    "ticket",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="answers",
                        to="tickets.ticket",
                    ),
                ),
            ],
        ),
    ]

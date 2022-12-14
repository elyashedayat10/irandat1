# Generated by Django 4.0.6 on 2022-07-29 09:55

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Setting",
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
                ("title", models.CharField(max_length=125)),
                ("icon", models.ImageField(upload_to="logo/")),
                ("description", models.TextField()),
            ],
            options={
                "abstract": False,
            },
        ),
    ]

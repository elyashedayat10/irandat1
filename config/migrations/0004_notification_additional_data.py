# Generated by Django 3.2.14 on 2022-08-30 15:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0003_notification'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='additional_data',
            field=models.JSONField(blank=True, null=True),
        ),
    ]
# Generated by Django 3.2.14 on 2022-09-02 11:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_rename_created_user_joined'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='promoted_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]

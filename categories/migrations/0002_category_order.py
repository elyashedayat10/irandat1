# Generated by Django 4.0.6 on 2022-08-02 21:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('categories', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='order',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]

# Generated by Django 4.0.6 on 2022-08-02 21:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('legalarticle', '0002_ipaddress_articlehit'),
    ]

    operations = [
        migrations.AddField(
            model_name='legalarticle',
            name='note',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]
# Generated by Django 3.2.14 on 2022-08-08 18:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('legalarticle', '0005_legalarticle_hits'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='articlehit',
            name='ip_address',
        ),
        migrations.RemoveField(
            model_name='legalarticle',
            name='hits',
        ),
        migrations.DeleteModel(
            name='IPAddress',
        ),
    ]

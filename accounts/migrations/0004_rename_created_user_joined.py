# Generated by Django 3.2.14 on 2022-09-02 11:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_auto_20220902_1110'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='created',
            new_name='joined',
        ),
    ]

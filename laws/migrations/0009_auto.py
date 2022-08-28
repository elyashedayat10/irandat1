from django.contrib.postgres.operations import TrigramExtension

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ('laws', '0008_auto_20220828_0719'),
    ]

    operations = [
        TrigramExtension(),
    ]

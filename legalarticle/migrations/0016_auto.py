from django.contrib.postgres.operations import TrigramExtension

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ('legalarticle', '0015_legalarticle__type'),
    ]

    operations = [
        TrigramExtension(),
    ]

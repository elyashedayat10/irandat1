from django.contrib.postgres.operations import TrigramExtension

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('legalarticle', '0015_legalarticle__type'),
    ]

    operations = [
        TrigramExtension(),
    ]

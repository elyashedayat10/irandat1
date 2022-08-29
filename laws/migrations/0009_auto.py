from django.contrib.postgres.operations import TrigramExtension

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('laws', '0008_auto_20220828_0719'),
    ]

    operations = [
        TrigramExtension(),
    ]

# Generated by Django 3.2.14 on 2022-09-08 14:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('legalarticle', '0017_legalarticle_tags'),
    ]

    operations = [
        migrations.AlterField(
            model_name='legalarticle',
            name='number',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]

# Generated by Django 3.2.14 on 2022-08-08 20:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("legalarticle", "0007_auto_20220808_1306"),
    ]

    operations = [
        migrations.AlterField(
            model_name="articlehit",
            name="previous_page",
            field=models.URLField(blank=True, null=True),
        ),
    ]

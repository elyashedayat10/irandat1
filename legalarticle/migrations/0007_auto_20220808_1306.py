# Generated by Django 3.2.14 on 2022-08-08 20:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("legalarticle", "0006_auto_20220808_1112"),
    ]

    operations = [
        migrations.AddField(
            model_name="articlehit",
            name="location",
            field=models.CharField(default="sdfd", max_length=125),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="articlehit",
            name="previous_page",
            field=models.URLField(default="www.ali.vom"),
            preserve_default=False,
        ),
    ]

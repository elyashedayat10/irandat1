# Generated by Django 3.2.14 on 2022-08-25 16:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("laws", "0006_chapter_parent"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="chapter",
            options={"ordering": ("-order",)},
        ),
        migrations.AlterModelOptions(
            name="law",
            options={"ordering": ("-order",)},
        ),
        migrations.AddField(
            model_name="chapter",
            name="order",
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="law",
            name="order",
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]

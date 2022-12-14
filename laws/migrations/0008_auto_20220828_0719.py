# Generated by Django 3.2.14 on 2022-08-28 07:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("laws", "0007_auto_20220825_1651"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="chapter",
            options={},
        ),
        migrations.AlterModelOptions(
            name="law",
            options={"ordering": ("order",)},
        ),
        migrations.AddField(
            model_name="chapter",
            name="level",
            field=models.PositiveIntegerField(default=1, editable=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="chapter",
            name="lft",
            field=models.PositiveIntegerField(default=1, editable=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="chapter",
            name="rght",
            field=models.PositiveIntegerField(default=1, editable=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="chapter",
            name="tree_id",
            field=models.PositiveIntegerField(db_index=True, default=1, editable=False),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="chapter",
            name="parent",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="children",
                to="laws.chapter",
            ),
        ),
    ]

# Generated by Django 3.2.14 on 2022-08-10 15:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("legalarticle", "0009_alter_articlehit_article"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="legalarticle",
            name="note",
        ),
    ]

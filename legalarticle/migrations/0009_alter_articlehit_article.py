# Generated by Django 3.2.14 on 2022-08-08 20:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('legalarticle', '0008_alter_articlehit_previous_page'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articlehit',
            name='article',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='hits', to='legalarticle.legalarticle'),
        ),
    ]

# Generated by Django 3.2.14 on 2022-08-23 12:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('laws', '0005_chapter'),
        ('legalarticle', '0013_auto_20220822_1519'),
    ]

    operations = [
        migrations.AddField(
            model_name='legalarticle',
            name='chapter',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='articles', to='laws.chapter'),
        ),
    ]

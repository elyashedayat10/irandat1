# Generated by Django 3.2.14 on 2022-08-10 15:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('legalarticle', '0010_remove_legalarticle_note'),
    ]

    operations = [
        migrations.CreateModel(
            name='Note',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField()),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notes', to='legalarticle.legalarticle')),
            ],
        ),
    ]
# Generated by Django 3.2.14 on 2022-08-23 12:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('laws', '0004_law_approval_authority'),
    ]

    operations = [
        migrations.CreateModel(
            name='Chapter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(max_length=125)),
                ('law', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='chapters', to='laws.law')),
            ],
        ),
    ]

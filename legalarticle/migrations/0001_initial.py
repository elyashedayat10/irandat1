# Generated by Django 4.0.6 on 2022-07-29 09:55

from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('laws', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='LegalArticle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('description', models.TextField()),
                ('approved', models.DateField()),
                ('number', models.PositiveIntegerField()),
                ('law', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='articles', to='laws.law')),
            ],
            options={
                'get_latest_by': 'modified',
                'abstract': False,
            },
        ),
    ]

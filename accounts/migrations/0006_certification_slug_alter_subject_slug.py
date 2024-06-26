# Generated by Django 5.0.6 on 2024-06-27 16:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_subject_slug_alter_subject_unique_together_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='certification',
            name='slug',
            field=models.SlugField(blank=True, max_length=150, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='subject',
            name='slug',
            field=models.SlugField(blank=True, max_length=150, null=True, unique=True),
        ),
    ]

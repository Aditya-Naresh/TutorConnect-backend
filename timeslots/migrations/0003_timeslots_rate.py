# Generated by Django 5.0.6 on 2024-11-23 07:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('timeslots', '0002_alter_timeslots_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='timeslots',
            name='rate',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=6),
        ),
    ]
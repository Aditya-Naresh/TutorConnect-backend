# Generated by Django 5.0.6 on 2024-12-18 18:13

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('timeslots', '0003_timeslots_rate'),
    ]

    operations = [
        migrations.CreateModel(
            name='WhiteboardState',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('drawing_data', models.JSONField(default=dict)),
                ('time_slot', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='timeslots.timeslots')),
            ],
        ),
    ]
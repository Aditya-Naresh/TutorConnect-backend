# Generated by Django 5.0.6 on 2024-11-11 14:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_amount',
            field=models.CharField(max_length=256),
        ),
    ]
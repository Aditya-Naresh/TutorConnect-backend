# Generated by Django 5.0.6 on 2024-10-08 21:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='auth_provider',
            field=models.CharField(choices=[('EMAIL', 'Email'), ('GOOGLE', 'Google')], default='EMAIL', max_length=50),
        ),
    ]
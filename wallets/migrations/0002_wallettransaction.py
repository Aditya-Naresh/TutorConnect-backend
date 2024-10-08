# Generated by Django 5.0.6 on 2024-07-25 12:50

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('timeslots', '0002_alter_timeslots_options_tuitionrequest'),
        ('wallets', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='WalletTransaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_type', models.CharField(choices=[('deposit', 'Deposit'), ('withdrawal', 'Withdrawal'), ('credit', 'Credit'), ('debit', 'Debit')], max_length=20)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=15)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('timeslot', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='timeslots.timeslots')),
                ('wallet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transactions', to='wallets.wallet')),
            ],
        ),
    ]

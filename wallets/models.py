from django.db import models
from accounts.models import User
from timeslots.models import TimeSlots
# Create your models here.

class Wallet(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)

    def __str__(self) -> str:
        return f"{self.owner.first_name}'s Wallet"


class WalletTransaction(models.Model):
    TRANSACTION_TYPE_CHOICES = (
        ('deposit', 'Deposit'),
        ('withdrawal', 'Withdrawal'),
        ('credit', 'Credit'),
        ('debit', 'Debit')
    )

    wallet = models.OneToOneField(Wallet, related_name='transactions', on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPE_CHOICES)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    timeslot = models.ForeignKey(TimeSlots, on_delete=models.CASCADE, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.wallet.owner.first_name} - {self.transaction_type}"
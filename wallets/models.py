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
    class TransactionType(models.TextChoices):
        DEPOSIT = "DEPOSIT", "DEPOSIT"
        WITHDRAW = "WITHDRAW", "WITHDRAW"

    wallet = models.ForeignKey(
        Wallet,
        related_name="transactions",
        on_delete=models.CASCADE,
    )
    transaction_type = models.CharField(
        max_length=20,
        choices=TransactionType.choices,
    )
    amount = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        unique=False,
    )
    timeslot = models.ForeignKey(
        TimeSlots,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.wallet.owner.first_name} - {self.transaction_type}"

    def save(self, *args, **kwargs):
        wallet = self.wallet

        if self.transaction_type == self.TransactionType.DEPOSIT:
            wallet.balance += self.amount
        elif self.transaction_type == self.TransactionType.WITHDRAW:
            if wallet.balance >= self.amount:
                wallet.balance -= self.amount
            else:
                raise ValueError("Insufficient funds for withdrawal")

        wallet.save()

        super(WalletTransaction, self).save(*args, **kwargs)

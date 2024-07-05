from django.db import models
from accounts.models import User
# Create your models here.

class Wallet(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)

    def __str__(self) -> str:
        return f"{self.owner.first_name}'s Wallet"

from rest_framework import serializers
from . models import Wallet
from accounts.models import User

class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = '__all__'
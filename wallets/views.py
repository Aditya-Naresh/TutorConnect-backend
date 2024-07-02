from django.shortcuts import render
from .serializers import WalletSerializer
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from . models import Wallet
# Create your views here.

class WalletView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = WalletSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        wallet, created = Wallet.objects.get_or_create(owner=self.request.user)
        return wallet
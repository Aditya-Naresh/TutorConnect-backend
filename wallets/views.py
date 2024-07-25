from .serializers import *
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from . models import *
# Create your views here.

class WalletView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = WalletSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        wallet, created = Wallet.objects.get_or_create(owner=self.request.user)
        return wallet
    


class TransactionListView(generics.ListCreateAPIView):
    queryset = WalletTransaction.objects.all()
    serializer_class = WalletTransactionSerializer

class TransactionDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = WalletTransaction.objects.all()
    serializer_class = WalletTransactionSerializer
    
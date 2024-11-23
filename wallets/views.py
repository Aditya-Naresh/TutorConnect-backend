from .serializers import WalletSerializer, WalletTransactionSerializer
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import WalletTransaction, Wallet

# Create your views here.


class WalletView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = WalletSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        wallet, created = Wallet.objects.get_or_create(owner=self.request.user)
        return wallet


class TransactionListView(generics.ListCreateAPIView):
    serializer_class = WalletTransactionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        wallet = Wallet.objects.get(owner=self.request.user)

        return WalletTransaction.objects.filter(wallet=wallet).order_by("-timestamp")

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)

        wallet = Wallet.objects.get(owner=request.user)

        response.data["wallet"] = {"id": wallet.pk, "balance": wallet.balance}

        return response


class TransactionDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = WalletTransaction.objects.all()
    serializer_class = WalletTransactionSerializer

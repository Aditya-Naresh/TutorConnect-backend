from django.urls import path
from . views import *

urlpatterns = [
    path('retrieve-update/', WalletView.as_view(), name='retrieve-update'),
    path('transactions/', TransactionListView.as_view(), name='transaction-list'),
    path('transactions/<int:pk>/', TransactionDetailView.as_view(), name='transaction-detail'),
]

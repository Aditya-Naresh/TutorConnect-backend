from django.urls import path
from . views import WalletView

urlpatterns = [
    path('retrieve-update/', WalletView.as_view(), name='retrieve-update'),
]

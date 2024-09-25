from django.urls import path
from .views import StartPaymentView, HandlePaymentSuccessView

urlpatterns = [
    path('start-payment/', StartPaymentView.as_view(), name='start_payment'),
    path('handle-payment-success/', HandlePaymentSuccessView.as_view(), name='handle_payment_success'),
]

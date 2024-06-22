from django.urls import path
from . views import RegisterUserView, EmailConfirmationView, LoginUserView
urlpatterns = [
    path("signup/", RegisterUserView.as_view(), name='register_user'),
    path("verify-email/", EmailConfirmationView.as_view(), name='email-verification'),
    path("login/", LoginUserView.as_view(), name='login'),
]

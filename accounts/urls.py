from django.urls import path
from . views import RegisterUserView, EmailConfirmationView, LoginUserView, PasswordResetRequestView,SetNewPasswordView
urlpatterns = [
    path("signup/", RegisterUserView.as_view(), name='register_user'),
    path("verify-email/", EmailConfirmationView.as_view(), name='email-verification'),
    path("login/", LoginUserView.as_view(), name='login'),
    path("reset-password/", PasswordResetRequestView.as_view(), name='password-reset'),
    path('set-new-password/', SetNewPasswordView.as_view(), name='set-new-password'),
]

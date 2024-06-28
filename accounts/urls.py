from django.urls import path
from . views import (
    RegisterUserView, EmailConfirmationView,
    LoginUserView, PasswordResetRequestView,
    SetNewPasswordView, SubjectView,
    CertificationView, 
    UserDetailsView
)
urlpatterns = [
    path("signup/", RegisterUserView.as_view(), name='register_user'),
    path("verify-email/", EmailConfirmationView.as_view(),
         name='email-verification'),
    path("login/", LoginUserView.as_view(), name='login'),
    path("reset-password/", PasswordResetRequestView.as_view(),
         name='password-reset'),
    path('set-new-password/', SetNewPasswordView.as_view(), name='set-new-password'),
    path('subject/', SubjectView.as_view(), name='subject'),
    path('subject/<id>', SubjectView.as_view(), name='subject-id'),
    path('certificates/', CertificationView.as_view(), name='certification'),
    path('certificates/<id>', CertificationView.as_view(), name='certification-id'),
    path('profile/<id>', UserDetailsView.as_view(), name='profile'),

]

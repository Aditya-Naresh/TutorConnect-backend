from rest_framework.generics import GenericAPIView
from . serializers import UserRegisterSerializer, EmailConfirmationSerializer, LoginSerializer
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from rest_framework.response import Response
from rest_framework import status
from .utils import send_normal_email
from django.db import IntegrityError
from rest_framework.exceptions import ValidationError
from rest_framework.views import exception_handler
from . models import User
# Create your views here.


class RegisterUserView(GenericAPIView):
    serializer_class = UserRegisterSerializer

    def post(self, request):
        user_data = request.data
        serializer = self.serializer_class(data=user_data)

        try:
            if serializer.is_valid(raise_exception=True):
                user = serializer.save()

                # Token for mail verification
                token_generator = PasswordResetTokenGenerator()
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                token = token_generator.make_token(user)
                site_domain = "http://localhost:5173"
                verification_link = f"{site_domain}/verify-email/{uid}/{token}/"
                email_body = f"Hi {user.get_full_name}, Use the link below to verify your email \n {verification_link}"
                mail_data = {
                    'email_body': email_body,
                    'email_subject': 'Email Verification',
                    'to_email': user.email
                }
                send_normal_email(mail_data)

                return Response({
                    'data': serializer.data,
                    'message': f"Hi {user.first_name}, Thanks for signing up! A verification link has been sent to your mail"
                }, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            if 'email' in e.detail:
                return Response({
                    'message': "A user with this email already exists please try to login"
                }, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#  Mail Confirmation


class EmailConfirmationView(GenericAPIView):
    serializer_class = EmailConfirmationSerializer

    def post(self, request):
        serializer = self.serializer_class(data = request.data)
        serializer.is_valid(raise_exception=True)
        
        uid = serializer.validated_data['uid']
        token = serializer.validated_data['token']

        try:
            user_id = force_str(urlsafe_base64_decode(uid))
            user = User.objects.get(pk = user_id)
            user.is_active = True
            user.is_verified = True
            user.save()
            return Response({
                'message': 'Email successfully verified'
            }, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({
                "error" : "Invalid link"
            }, status=status.HTTP_400_BAD_REQUEST)
        

# Login
class LoginUserView(GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'request':request})
        if serializer.is_valid(raise_exception=True):
            return Response(serializer.data, status=status.HTTP_200_OK)
        

# Forgot Password

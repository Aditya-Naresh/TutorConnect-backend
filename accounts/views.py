from rest_framework.generics import GenericAPIView
from . serializers import UserRegisterSerializer
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from rest_framework.response import Response
from rest_framework import status
from .utils import send_normal_email
# Create your views here.

class RegisterUserView(GenericAPIView):
    serializer_class = UserRegisterSerializer

    def post(self, request):
        user_data = request.data
        serializer = self.serializer_class(data = user_data)

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
                'email_body' : email_body,
                'email_subject': 'Email Verification',
                'to_email': user.email
            }
            send_normal_email(mail_data)

            return Response({
                'data' : serializer.data,
                'message': f"Hi {user.first_name}, Thanks for signing up! A verification link has been sent to your mail"
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from . serializers import *
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from rest_framework.response import Response
from rest_framework import status
from .utils import send_normal_email
from django.db import IntegrityError, transaction
from rest_framework.exceptions import ValidationError
from rest_framework.views import exception_handler
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated
from . models import *
from rest_framework import generics , status
from .permissions import IsOwnerTutorOnly
from PIL import Image
import base64
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import environ

env = environ.Env()
environ.Env.read_env()

# Create your views here.

class RegisterUserView(APIView):
    def post(self, request):
        is_tutor = request.data['is_tutor']
        email = request.data['email']
        first_name = request.data['first_name']
        last_name = request.data['last_name']
        password = request.data['password']
        confirm_password = request.data['password']
        try:
            user_model = Tutor if is_tutor else Student
            role = User.Role.TUTOR if is_tutor else User.Role.STUDENT
            user = user_model.objects.create(
                email = email,
                first_name = first_name,
                last_name = last_name,
                role = role

            )

            user.set_password(password)
            user.is_active = False
            user.save()
            print ("User:", user.pk, user.role)

            if is_tutor:
            
                # Creating Certifications
                certifications_data = request.data['certifications']
                for cert in certifications_data:
                    image = self._convert_image(cert['image'])
                    print("image", image)
                    certificate = Certification.objects.create(
                        title = cert['title'],
                        image = image,
                        owner = user
                    )

                    print("certificate:", certificate.title)
                # Adding subjects
                subjects_data = request.data['subjects']
                for sub in subjects_data:
                    subject = Subject.objects.create(
                        name = sub,
                        owner = user
                    )
                    print("subject: ", subject)
                rate = request.data['rate']
                user.rate = float(rate)
                user.is_submitted = True
                
                user.save()
            self._send_mail(user)
            return Response({"message": "User created successfully."}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error" : "Failed to create user. Please try again."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def _send_mail(self, user):
        token_generator = PasswordResetTokenGenerator()
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = token_generator.make_token(user)
        site_domain = "http://localhost:5173"
        verification_link = f"{site_domain}/verify-email/{uid}/{token}/"
        name = f"{user.first_name} {user.last_name}"
        email_body = f"Hi {name}, Use the link below to verify your email \n {verification_link}"
        mail_data = {
                    'email_body': email_body,
                    'email_subject': 'Email Verification',
                    'to_email': user.email
                }
        return send_normal_email(mail_data)
    

    def _convert_image(self, data):
        try:
            image_data = data.split(',')[1]
            bytes_decoded = base64.b64decode(image_data)
            image = Image.open(BytesIO(bytes_decoded))
            output = BytesIO()
            image = image.convert('RGB')
            image.save(output, format='JPEG')
            output.seek(0)
            return InMemoryUploadedFile(output, 'ImageField', 'temp.jpg', 'image/jpeg', output.getbuffer().nbytes, None)
        except Exception as e:
            raise ValueError("Invalid Image Format")

#  Mail Confirmation


class EmailConfirmationView(GenericAPIView):
    serializer_class = EmailConfirmationSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        uid = serializer.validated_data['uid']
        token = serializer.validated_data['token']

        try:
            user_id = force_str(urlsafe_base64_decode(uid))
            user = User.objects.get(pk=user_id)
            user.is_active = True
            user.is_verified = True
            user.save()
            return Response({
                'message': 'Email successfully verified'
            }, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({
                "error": "Invalid link or user does not exist."
            }, status=status.HTTP_400_BAD_REQUEST)


# Login
class LoginUserView(GenericAPIView):
    serializer_class = LoginSerializer
    queryset = User.objects.all()

    def post(self, request):
        print("REQUEST:", request)
        serializer = self.serializer_class(
            data=request.data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            return Response(serializer.data, status=status.HTTP_200_OK)


# Forgot Password
class PasswordResetRequestView(GenericAPIView):
    serializer_class = PasswordResetSerializer

    def post(self, request):
        serializer = self.serializer_class(
            data=request.data, context={'request': request})
        try:
            if serializer.is_valid(raise_exception=True):
                return Response({
                    'message': "A link has been sent to your mail to reset your password"
                }, status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response({
                "message": "Email address is not registered"
            }, status=status.HTTP_400_BAD_REQUEST)


class SetNewPasswordView(GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            password = serializer.validated_data['password']
            confirm_password = serializer.validated_data['confirm_password']
            uidb64 = serializer.validated_data['uidb64']
            token = serializer.validated_data['token']

            if password != confirm_password:
                raise serializers.ValidationError("Passwords do not match")

            User = get_user_model()

            try:
                user_id = force_str(urlsafe_base64_decode(uidb64))
                user = User.objects.get(pk=user_id)
            except (ValueError, ObjectDoesNotExist):
                raise AuthenticationFailed("Invalid reset link")

            if not default_token_generator.check_token(user, token):
                raise AuthenticationFailed(
                    "Reset link is invalid or has expired")

            user.set_password(password)
            user.save()

            return Response({'success': True, 'message': "Password reset successful"}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#  Logout
class LogoutUserView(GenericAPIView):
    serializer_class = LogoutSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
    



# Profile VIew
class UserDetailsView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    lookup_field = 'id'
    serializer_class = UpdateProfileSerializer
    permission_classes = [IsAuthenticated]
   


# Tutor Profile
class SubjectView(generics.ListCreateAPIView, generics.RetrieveDestroyAPIView):
    permission_classes = [IsOwnerTutorOnly]
    serializer_class = SubjectSerializer
    lookup_field = 'id'

    def get_queryset(self):
        return Subject.objects.filter(owner = self.request.user)
    
    def perform_create(self, serializer):
        try:
            serializer.save(owner=self.request.user)
        except IntegrityError:
            raise serializers.ValidationError(
                {"detail": "This subject already exists for this tutor."})


class CertificationView(generics.ListCreateAPIView, generics.RetrieveDestroyAPIView):
    permission_classes = [IsOwnerTutorOnly]
    serializer_class = CertificationSerializer
    lookup_field = 'id'

    def perform_create(self, serializer):
        try:
            serializer.save(owner=self.request.user)
        except IntegrityError:
            raise serializers.ValidationError(
                {"detail": "This subject already exists for this tutor."})
        
    def get_queryset(self):
        return Certification.objects.filter(owner = self.request.user)
    
# Google Authentication

class GoogleAuthenticationView(APIView):
    serializer_class = LoginSerializer
    queryset = User.objects.all()
    
    def post(self, request):
        email = request.data['email']
        try:
            user = User.objects.get(email = email)
            # if user.auth_provider == User.a
            data = self._login(user)
            print("Data: ", data)
            if "error" in data:
                return Response(data, status=status.HTTP_403_FORBIDDEN)
            return Response(data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            user = self._signup(request)
            data = self._login(user)
            return Response(data, status=status.HTTP_201_CREATED)


    def _signup(self, request):
        email = request.data['email']
        first_name = request.data['first_name']
        last_name = request.data['last_name']

        try:
            user = User.objects.create(
                email = email,
                first_name = first_name,
                last_name = last_name,
                auth_provider = User.AuthProviders.GOOGLE,
                role = User.Role.NEW
            )
            user.set_password(env('GOOGLE_AUTH_PASSWORD'))
            user.save()
            return user
        except Exception as e:
            return Response({"error" : "Falied to create user. Please try again"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

    def _login(self, user):
        if user.is_blocked:
            return {"error": "Login failed. Please contact support."}
    
        try:
            user_tokens = user.tokens()
            return {
                "id": user.pk,
                "email": user.email,
                "full_name": user.get_full_name(),
                "role": user.role,
                "access_token": str(user_tokens.get("access")),
                "refresh_token": str(user_tokens.get("refresh")),
            }
        except Exception as e:
            return {"error": f"Token generation failed: {str(e)}"}

from rest_framework import serializers
from . models import User, Student, Tutor, Subject, Certification
from django.contrib.auth import authenticate, get_user_model
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_str, force_bytes
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.db import IntegrityError
from rest_framework.exceptions import ValidationError
from .utils import send_normal_email
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from rest_framework.fields import CurrentUserDefault


# User SignUp

class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=68, min_length=6, write_only=True)
    confirm_password = serializers.CharField(
        max_length=68, min_length=6, write_only=True)
    is_tutor = serializers.BooleanField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'first_name', "last_name",
            "password", "confirm_password", "is_tutor"]

    def validate(self, attrs):
        password = attrs.get('password', "")
        confirm_password = attrs.get('confirm_password', "")
        if password != confirm_password:
            raise serializers.ValidationError("Passwords do not match")
        return attrs

    def create(self, validated_data):
        is_tutor = validated_data.pop("is_tutor", False)
        user_model = Tutor if is_tutor else Student

        try:
            user = user_model.objects.create_user(
                email=validated_data['email'],
                first_name=validated_data['first_name'],
                last_name=validated_data['last_name'],
                password=validated_data['password']
            )
        except IntegrityError:
            raise ValidationError(
                {"message": "A user with this email already exists."})

        return user


# Mail Confirmation Serializer

class EmailConfirmationSerializer(serializers.Serializer):
    uid = serializers.CharField(min_length=1, write_only=True)
    token = serializers.CharField(min_length=3, write_only=True)


# Login Serializer
class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, min_length=6)
    password = serializers.CharField(max_length=68, write_only=True)
    full_name = serializers.CharField(max_length=255, read_only=True)
    access_token = serializers.CharField(max_length=255, read_only=True)
    refresh_token = serializers.CharField(max_length=255, read_only=True)
    role = serializers.CharField(max_length=100, read_only=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'full_name',
            'role', 'access_token', 'refresh_token']

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        request = self.context.get('request')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise AuthenticationFailed("Invalid credentials, try again")

        if user.is_blocked:
            raise AuthenticationFailed("Your account is blocked, please contact support")
    
        if not user.check_password(password):
            raise AuthenticationFailed("Invalid credentials, try again")
        user_tokens = user.tokens()
        return{
            "email":user.email,
            "full_name":user.get_full_name,
            "role": user.role,
            "access_token": str(user_tokens.get('access')),
            "refresh_token": str(user_tokens.get('refresh'))
        }
    

# Password Reset
class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)

    class Meta:
        fields = ['email']
    
    def validate(self, attrs):
        email = attrs.get('email')
        if User.objects.filter(email = email).exists():
            user = User.objects.get(email=email)
            uidb64 = urlsafe_base64_encode(force_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            request = self.context.get('request')
            site_domain = "http://localhost:5173"
            abslink=f"{site_domain}/reset-password/{uidb64}/{token}"
            email_body = f"Hi use the link below to reset your password \n {abslink}"

            data = {
                'email_body': email_body,
                'email_subject': "Reset Password",
                'to_email': user.email
            }
            send_normal_email(data)
        else:
            raise ValidationError("Email address is not registered")

        return super().validate(attrs)
    

class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=100, min_length=6, write_only=True)
    confirm_password = serializers.CharField(max_length=100, min_length=6, write_only=True)
    uidb64 = serializers.CharField(min_length=1, write_only=True)
    token = serializers.CharField(min_length=3, write_only=True)

    def validate(self, attrs):
        password = attrs.get('password')
        confirm_password = attrs.get('confirm_password')
        uidb64 = attrs.get('uidb64')
        token = attrs.get('token')

        if password!= confirm_password:
            raise serializers.ValidationError("Passwords do not match")

        return attrs



class LogoutSerializer(serializers.Serializer):
    refresh_token=serializers.CharField()
    default_error_message = {
        'bad_token': ('Token is Invalid or has expired')
    }

    def validate(self, attrs):
        self.token = attrs.get('refresh_token')
        return attrs
    
    def save(self, **kwargs):
        try:
            token = RefreshToken(self.token)
            token.blacklist()
        except TokenError:
            return self.fail('bad_token')
        



class SubjectSerializer(serializers.ModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(default = CurrentUserDefault(), read_only = True)
    slug = serializers.CharField(max_length = 200, read_only = True)

    class Meta:
        model = Subject
        fields = '__all__'




class CertificationSerializer(serializers.ModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(default = CurrentUserDefault(), read_only = True)
    slug = serializers.CharField(max_length = 200, read_only = True)

    class Meta:
        model = Certification
        fields = '__all__'



class UpdateProfileSerializer(serializers.ModelSerializer):
    pass
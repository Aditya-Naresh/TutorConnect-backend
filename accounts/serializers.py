from rest_framework import serializers
from . models import User, Student, Tutor
from django.contrib.auth import authenticate, get_user_model
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_str, force_bytes
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.db import IntegrityError
from rest_framework.exceptions import ValidationError


# User SignUp

class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length = 68, min_length = 6, write_only = True)
    confirm_password = serializers.CharField(max_length = 68, min_length = 6, write_only = True)
    is_tutor = serializers.BooleanField(write_only = True)
    class Meta:
        model = User
        fields = ['email', 'first_name', "last_name", "password", "confirm_password", "is_tutor"]

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
            raise ValidationError({"message": "A user with this email already exists."})

        return user
    

# Mail Confirmation Serializer

class EmailConfirmationSerializer(serializers.Serializer):
    uid = serializers.CharField(min_length = 1, write_only = True)
    token = serializers.CharField(min_length = 3, write_only = True)
    
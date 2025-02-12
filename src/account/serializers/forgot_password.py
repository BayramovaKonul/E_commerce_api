from rest_framework import serializers
from rest_framework.validators import ValidationError
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from ..models import ForgotPasswordTokenModel
from django.utils import timezone


User=get_user_model()

class RequestForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("No user found with this email address.")
        return value


class ForgotPasswordSerializer(serializers.Serializer):
    token = serializers.UUIDField(required=True)  # Add token field
    new_password = serializers.CharField(required=True, write_only=True, min_length=8)
    confirm_password = serializers.CharField(required=True, write_only=True)

    def validate(self, data):
        token = data.get('token')
        new_password = data.get('new_password')
        confirm_password = data.get('confirm_password')

        # Validate token existence and expiration
        token_obj = ForgotPasswordTokenModel.objects.filter(token=token, is_used=False).first()
        if not token_obj or token_obj.is_expired():
            raise serializers.ValidationError({"token": "Invalid or expired token."})
        
        if new_password != confirm_password:
            raise serializers.ValidationError({"confirm_password": "Passwords do not match."})  
        
        # to use in save method
        self.context['token_obj'] = token_obj

        validate_password(new_password)
        return data

    def save(self, **kwargs):
        user = self.context.get('user')  # Retrieve user from context
        token_obj = self.context.get('token_obj')  # Retrieve token from context

        if not user or not token_obj:
            raise serializers.ValidationError("Invalid request.")
        
        user.set_password(self.validated_data['new_password'])
        user.save()

        # Mark the token as used and expired
        token_obj.is_used = True
        token_obj.is_expired = timezone.now()
        token_obj.save()

        
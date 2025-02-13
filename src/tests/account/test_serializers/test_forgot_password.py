import pytest
from account.serializers import RequestForgotPasswordSerializer, ForgotPasswordSerializer
from account.models import ForgotPasswordTokenModel
from django.utils import timezone
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError
from django.contrib.auth.hashers import check_password
from ...confest import user

@pytest.mark.django_db
class TestRequestForgotPasswordSerializer:
    def test_forgot_password_request_with_valid_email(self, user):
        """Test valid email for password reset request"""

        data = {"email": user.email}
        token = ForgotPasswordTokenModel.objects.create(user=user)

        serializer = RequestForgotPasswordSerializer(data=data)
        assert serializer.is_valid(), serializer.errors
        assert token.is_used is False
        assert token.expired_at > token.created_at
        assert token.user.email == user.email

    
    def test_forgot_password_request_with_invalid_email(self, user):
        """Test invalid email for password reset request"""
        
        data = {"email": "invalid_email@gmail.com"}
        serializer = RequestForgotPasswordSerializer(data=data)
        
        assert not serializer.is_valid()

        assert "email" in serializer.errors
        assert serializer.errors["email"] == ["No user found with this email address."]


    def test_valid_token_and_password(self, user):
        """Test valid token and password reset process"""
        token = ForgotPasswordTokenModel.objects.create(user=user)

        data = {
            "token": str(token.token),
            "new_password": "mynewpassword123",
            "confirm_password": "mynewpassword123",
        }

        serializer = ForgotPasswordSerializer(data=data)
        assert serializer.is_valid()
        serializer.context["user"] = user
        serializer.context["token_obj"] = token
        serializer.save()

        assert user.check_password("mynewpassword123")
        assert token.is_expired < timezone.now()
        assert token.is_used == True


    def test_invalid_token_and_valid_password(self, user):
        """Test invalid token for password reset"""

        data = {
            "token": "invalid_token",
            "new_password": "mynewpassword123",
            "confirm_password": "mynewpassword123",
        }

        serializer = ForgotPasswordSerializer(data=data)
        assert not serializer.is_valid()
        assert "token" in serializer.errors
        assert serializer.errors["token"] == ["Must be a valid UUID."]


    def test_expired_token_and_valid_password(self, user):
        """Test expired token for password reset"""

        data = {
            "token": "73af13ba-0f7d-4998-affa-db7b697d00c2",
            "new_password": "mynewpassword123",
            "confirm_password": "mynewpassword123",
        }

        serializer = ForgotPasswordSerializer(data=data)
        assert not serializer.is_valid()
        assert "token" in serializer.errors
        assert serializer.errors["token"] == ["Invalid or expired token."]


    def test_valid_token_and_unmatched_password(self, user):
        """Test valid token and unmatched password for password reset"""

        token = ForgotPasswordTokenModel.objects.create(user=user)

        data = {
            "token": str(token.token),
            "new_password": "mynewpassword123",
            "confirm_password": "mynewpassword1234",
        }

        serializer = ForgotPasswordSerializer(data=data)
        assert not serializer.is_valid()
        assert "confirm_password" in serializer.errors
        assert serializer.errors["confirm_password"] == ["Passwords do not match."]

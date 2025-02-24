import pytest
from rest_framework import status
from django.contrib.auth.hashers import check_password
from account.serializers import UserRegisterSerializer
from ...confest import user, validation_token
from django.core import mail
from account.models import ValidateUserTokenModel
from account.serializers import UserValidationSerializer
from datetime import timedelta
from django.utils.timezone import now
from rest_framework import serializers
import uuid

@pytest.mark.django_db
class TestUserRegisterSerializer:

    def test_register_user_with_valid_data(self):
        """Test creating a user with valid data"""

        data = {
            'first_name': 'Konul',
            'last_name': 'Bayramova',
            'email': 'konul@example.com',
            'password1': 'Password123',
            'password2': 'Password123'
        }

        serializer = UserRegisterSerializer(data=data)
        assert serializer.is_valid()
        
        # Ensure the user is created
        user = serializer.save()
        
        assert user.first_name == data["first_name"]
        assert user.last_name == data["last_name"]
        assert user.email == data["email"]
        assert check_password(data["password1"], user.password)

    def test_register_user_with_duplicate_email(self, user):
        """Test registration with an email that already exists"""

        data = {
            'first_name': 'Konul',
            'last_name': 'Bayramova',
            'email': user.email,  # Using an existing email
            'password1': 'Password123',
            'password2': 'Password123'
        }

        serializer = UserRegisterSerializer(data=data)
        assert not serializer.is_valid()
        
        # Assert error message for email field
        assert "email" in serializer.errors
        assert serializer.errors["email"] == ["User with this email already exists."]


    def test_register_user_with_password_mismatch(self):
        """Test registration with non-matching passwords"""

        data = {
            'first_name': 'Konul',
            'last_name': 'Bayramova',
            'email': 'konul@example.com',
            'password1': 'Password123',
            'password2': 'Password456'
        }

        serializer = UserRegisterSerializer(data=data)
        assert not serializer.is_valid()

        assert "password2" in serializer.errors
        assert serializer.errors["password2"] == ["Passwords must match."]


    def test_user_validation_email(self):
        """Test receiving email validatin after registration"""

        data = {
            'first_name': 'Konul',
            'last_name': 'Bayramova',
            'email': 'konul@example.com',
            'password1': 'Password123',
            'password2': 'Password123'
        }

        serializer = UserRegisterSerializer(data=data)
        assert serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Assert that an email was sent
        assert len(mail.outbox) == 1  # For only email validation since it was sent first
        email = mail.outbox[0]
            
        # Verify the email details (subject, recipient, and body)
        assert mail.outbox[0].subject == "Email Validation" # first email in the box
        assert email.to == [user.email]


    @pytest.mark.django_db
    def test_user_validation_serializer_with_valid_token(self, user, validation_token):
        """Test the UserValidationSerializer with valid tokens"""

        serializer = UserValidationSerializer(data={"token": validation_token.token})
        assert serializer.is_valid()
        assert serializer.validated_data["token"] == validation_token


    @pytest.mark.django_db
    def test_user_validation_serializer_with_expired_token(self, user):
        """Test the UserValidationSerializer with expired tokens"""

        expired_token = ValidateUserTokenModel.objects.create(
            token=str(uuid.uuid4()),
            is_used=False,
            created_at=now() - timedelta(days=2), 
            expired_at=now() - timedelta(days=1), 
            user=user
        )

        serializer = UserValidationSerializer(data={"token": expired_token.token})
        assert not serializer.is_valid()

        assert "token" in serializer.errors
        assert str(serializer.errors["token"][0]) == "{'Invalid or expired token.'}"






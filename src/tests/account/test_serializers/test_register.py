import pytest
from rest_framework.exceptions import ValidationError
from rest_framework import status
from django.contrib.auth.hashers import check_password
from account.serializers import UserRegisterSerializer
from account.models import CustomUserModel
from ...confest import user


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



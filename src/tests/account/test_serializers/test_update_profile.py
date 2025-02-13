import pytest
from django.contrib.auth import get_user_model
from account.serializers import UserProfileSerializer
from django.core.exceptions import ValidationError
from ...confest import user


@pytest.mark.django_db

def test_update_user_profile(user):
    """Test using UserProfileSerializer to update user profile"""


    profile_new_data={
        "birthday":"1999-03-08",
        "phone_number" : "+994557415171",
        "first_name":"test_update",
        "last_name":"check_update"
    }

    serializer=UserProfileSerializer(user.profile, data=profile_new_data)

    assert serializer.is_valid(), serializer.errors
    updated_user_profile=serializer.save()

    
    assert updated_user_profile.user.first_name == profile_new_data["first_name"]
    assert updated_user_profile.user.last_name == profile_new_data["last_name"]
    assert str(updated_user_profile.birthday) == profile_new_data["birthday"]
    assert str(updated_user_profile.phone_number) == profile_new_data["phone_number"]


@pytest.mark.django_db
def test_validate_phone_number_valid(user):
        """Test phone number normalization and validation."""
        # Valid phone numbers
        valid_phone_numbers = [
            "+994501234567",
            "0501234567",
            "501234567"
        ]
        for phone_number in valid_phone_numbers:
            data = {'phone_number': phone_number}
            serializer = UserProfileSerializer(instance=user.profile, data=data)

            # Validate the phone number
            assert serializer.is_valid(), f"Validation failed for {phone_number}: {serializer.errors}"
            validated_phone_number = serializer.validated_data['phone_number']
            assert validated_phone_number == "+994501234567", f"Failed for {phone_number}. Expected '+994501234567' but got {validated_phone_number}"


@pytest.mark.django_db
def test_validate_phone_number_invalid(user):
        """Test phone number normalization and validation with invalid phone_number"""
        # Valid phone numbers
        valid_phone_numbers = [
            "+99450123456744",
            "12345678",
            "08550123459",
            "invalid_phone_number"
        ]
        for phone_number in valid_phone_numbers:
            data = {'phone_number': phone_number}
            serializer = UserProfileSerializer(instance=user.profile, data=data)

            # Validate the phone number
            assert not serializer.is_valid()
            assert "phone_number" in serializer.errors
            assert serializer.errors["phone_number"] == ["Invalid phone number format. Use +994XXXXXXXXX, 05XXXXXXXX, or 5XXXXXXXX."]
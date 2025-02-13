import pytest
from rest_framework.exceptions import ValidationError
from rest_framework import status
from django.contrib.auth.hashers import check_password
from account.serializers import ResetPasswordSerializer
from ...confest import user

@pytest.mark.django_db

def test_reset_password_with_matched_passwords(user):
    """Test using ResetPasswordSerializer to reset user password"""


    new_password_data={
        "old_password":"1234",
        "new_password" : "12345kkk",
        "confirm_password":"12345kkk",
    }

    serializer=ResetPasswordSerializer(data=new_password_data, context={'user': user})

    assert serializer.is_valid(), serializer.errors
    reset_password=serializer.save()

    
    assert user.check_password(new_password_data["new_password"])



@pytest.mark.django_db

def test_reset_password_with_unmatched_passwords(user):
    """Test using ResetPasswordSerializer to reset user password with unmatched passwords"""


    new_password_data={
        "old_password":"1234",
        "new_password" : "12345kkbb",
        "confirm_password":"12345kkk",
    }

    serializer=ResetPasswordSerializer(data=new_password_data, context={'user': user})

    assert not serializer.is_valid()

    assert "confirm_password" in serializer.errors
    assert serializer.errors["confirm_password"] == ["Passwords do not match."]


@pytest.mark.django_db

def test_reset_password_with_short_passwords(user):
    """Test using ResetPasswordSerializer to reset user password with short passwords"""


    new_password_data={
        "old_password":"1234",
        "new_password" : "12345",
        "confirm_password":"12345",
    }

    serializer=ResetPasswordSerializer(data=new_password_data, context={'user': user})

    assert not serializer.is_valid()

    assert "new_password" in serializer.errors
    assert serializer.errors["new_password"] == ["Ensure this field has at least 8 characters."]


@pytest.mark.django_db
def test_reset_password_with_invalid_old_password(user):
    """Test using ResetPasswordSerializer to reset user password with invalid old password"""


    new_password_data={
        "old_password":"12345",
        "new_password" : "12345kkk",
        "confirm_password":"12345kkk",
    }

    serializer=ResetPasswordSerializer(data=new_password_data, context={'user': user})

    assert not serializer.is_valid()

    assert "old_password" in serializer.errors
    assert serializer.errors["old_password"] == ["The old password is incorrect."]

import pytest 
from django.urls import reverse
from rest_framework import status
from ...confest import anonymous_client, user
from django.conf import settings


@pytest.mark.django_db
def test_register_view_with_valid_credentials(anonymous_client):
    """Test that user registers with valid credentials """
    from django.utils.translation import activate
    activate('en')  # Ensures test runs in English without unwanted locale prefix

    url = reverse("register")

    data={
        "email":'test_valid@gmail.com',
        "first_name": 'test',
        "last_name": 'check',
        "password1": "1234",
        "password2": "1234"
    }

    res = anonymous_client.post(url, data=data,format='json')

    assert res.status_code == status.HTTP_201_CREATED
    assert res.data["message"] == "You registered successfully"


@pytest.mark.django_db
def test_register_view_with_unmatched_passwords(anonymous_client):
    """Test that it raises error when entered passwords don't match """
    url = reverse("register")

    data={
        "email":'test_unmatched@gmail.com',
        "first_name": 'test',
        "last_name": 'check',
        "password1": "1234",
        "password2": "12345"
    }

    res = anonymous_client.post(url, data=data,format='json')

    assert not res.status_code == status.HTTP_201_CREATED
    assert res.data['password2'] == ["Passwords must match."]


@pytest.mark.django_db
def test_register_view_with_unique_emails(user, anonymous_client):
    """Test that it raises error when entered email is not unique """
    url = reverse("register")

    data={
        "email":'test@gmail.com',
        "first_name": 'test',
        "last_name": 'check',
        "password1": "1234",
        "password2": "1234"
    }

    res = anonymous_client.post(url, data=data,format='json')

    assert not res.status_code == status.HTTP_201_CREATED
    assert res.data['email'] == ["User with this email already exists."]


@pytest.mark.django_db
def test_register_view_with_missing_fields(anonymous_client):
    """Test that it raises an error when required fields are missing"""
    url = reverse("register")

    data = {
        "email": "test_missing@gmail.com",
        "password1": "1234",
        "password2": "1234"
    }  # Missing first_name and last_name

    res = anonymous_client.post(url, data=data, format="json")

    assert not res.status_code == status.HTTP_201_CREATED
    assert "first_name" in res.data
    assert res.data["first_name"] == ["This field is required."]
    assert "last_name" in res.data
    assert res.data["last_name"] == ["This field is required."]


@pytest.mark.django_db
def test_register_view_with_invalid_email(anonymous_client):
    """Test that it raises an error for invalid email format"""
    url = reverse("register")

    data = {
        "email": "invalid-email",
        "first_name": "test",
        "last_name": "check",
        "password1": "1234",
        "password2": "1234"
    }

    res = anonymous_client.post(url, data=data, format="json")

    assert not res.status_code == status.HTTP_201_CREATED
    assert "email" in res.data
    assert res.data["email"] == ["Enter a valid email address."]


# SINCE WE ARE IN DEVELOPMENT STAGE, I DISABLED PASSWORD VALIDATORS, BUT USUALLY IT IS FOR WEAK PASSWORDS

if settings.DEBUG == False:

    @pytest.mark.django_db
    def test_register_view_with_weak_password(anonymous_client):
        """Test that weak passwords are rejected"""


        url = reverse("register")

        data = {
            "email": "testweak@gmail.com",
            "first_name": "Test",
            "last_name": "Weak",
            "password1": "1234",
            "password2": "1234"
        }

        res = anonymous_client.post(url, data=data, format="json")

        assert not res.status_code == 200
        assert "password1" in res.data 
        assert res.data["password1"] == ["Weak password"]








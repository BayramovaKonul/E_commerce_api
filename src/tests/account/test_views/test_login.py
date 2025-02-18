import pytest 
from django.urls import reverse
from rest_framework import status
from ...confest import anonymous_client, user
from rest_framework_simplejwt.tokens import RefreshToken

@pytest.mark.django_db
def test_token_obtain_view_with_valid_credentials(user, anonymous_client):
    """Test getting access and refresh token using login credentials"""
    from django.utils.translation import activate
    activate('en')  # Ensures test runs in English without unwanted locale prefix

    url = reverse("token_obtain_pair")
    # user credentials
    data={
        "email":user.email,
        "password":"1234"
    }

    res=anonymous_client.post(url, data=data, format='json')
    print(res)

    assert res.status_code==status.HTTP_200_OK

    assert 'access' in res.data
    assert 'refresh' in res.data

    assert len(res.data["access"]) > 0
    assert len(res.data["refresh"]) > 0



@pytest.mark.django_db
def test_token_obtain_view_with_invalid_credentials(user, anonymous_client):

    """Test it raises error when invalid email is entered"""
    url = reverse("token_obtain_pair")
    # user credentials
    data={
        "email":"invalid_email@gmail.com",
        "password":"1234"
    }

    res=anonymous_client.post(url, data=data, format='json')

    assert not res.status_code==status.HTTP_200_OK
    assert res.data["detail"] == "No active account found with the given credentials"



@pytest.mark.django_db
def test_token_refresh_view_with_valid_credentials(user, anonymous_client):
    """Test getting access token using logged in user's refresh token"""

    refresh = RefreshToken.for_user(user)
    print(refresh)

    # Endpoint and payload
    url = reverse("token_refresh")
    data = {
        "refresh": str(refresh)
    }
    res=anonymous_client.post(url, data=data, format='json')

    assert res.status_code==status.HTTP_200_OK
    assert 'access' in res.data
    assert len(res.data["access"]) > 0



@pytest.mark.django_db
def test_token_refresh_view_with_invalid_credentials(user, anonymous_client):
    """Test getting error when using invalid or expired refresh token"""
    
    # Create an invalid or expired refresh token 
    invalid_refresh_token = "invalid_refresh_token"

    url = reverse("token_refresh")
    data = {
        "refresh": invalid_refresh_token
    }
    
    res = anonymous_client.post(url, data=data, format='json')

    assert not res.status_code == status.HTTP_200_OK
    assert res.data["detail"] == "Token is invalid or expired"

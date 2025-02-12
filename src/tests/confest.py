import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

@pytest.fixture
# a user that has not logged in yet
def anonymous_client():
    return APIClient()


@pytest.fixture
def user():
    return get_user_model().objects.create_user(email='test@gmail.com',
                                                first_name = "konul",
                                                last_name = "bayramova",
                                                password='1234')


@pytest.fixture
# a user that has already logged in
def authenticated_client(user):
    # get refresh token for the logged in user
    refresh=RefreshToken.for_user(user)
    client=APIClient()
    # get access token using the refresh token
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
    return client, refresh

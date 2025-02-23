import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.files.uploadedfile import SimpleUploadedFile
from store.models import StoreModel
from io import BytesIO
from PIL import Image

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
def another_user():
    """Fixture for creating a test user who doesn't own the store"""
    return get_user_model().objects.create_user(email='test2@gmail.com',
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
    return client


@pytest.fixture
def store(user):
    # Create a valid image using PIL
    image_file = BytesIO()
    image = Image.new('RGB', (100, 100), color=(73, 109, 137))
    image.save(image_file, format='JPEG')
    image_file.seek(0)

    image = SimpleUploadedFile("test_picture.jpg", image_file.read(), content_type="image/jpeg")

    store = StoreModel.objects.create(
        owner=user,
        name='Test Store',
        description='This is a test store.',
        address='123 Test Street',
        website='https://teststore.com',
        picture=image
    )
    return store

@pytest.fixture
def store_data(user):
    """Sample store data for testing"""
     # Create a valid image using PIL
    image_file = BytesIO()
    image = Image.new('RGB', (100, 100), color=(73, 109, 137))
    image.save(image_file, format='JPEG')
    image_file.seek(0)

    image = SimpleUploadedFile("test_picture.jpg", image_file.read(), content_type="image/jpeg")
    return {
        'name': 'Test Store2',
        'description': 'This is a new test store.',
        'address': '1234 Test Street',
        'website': 'https://teststore2.com',
        'picture': image,
        'owner': user
        }
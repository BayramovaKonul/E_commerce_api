import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.files.uploadedfile import SimpleUploadedFile
from store.models import StoreModel
from products.models import CategoryModel, ProductModel, ProductImageModel
from io import BytesIO
from PIL import Image
import uuid
from account.models import ValidateUserTokenModel
from django.core.files.uploadedfile import InMemoryUploadedFile

@pytest.fixture
# a user that has not logged in yet
def anonymous_client():
    return APIClient()


@pytest.fixture
def user():
    return get_user_model().objects.create_user(email='test@gmail.com',
                                                first_name = "konul",
                                                last_name = "bayramova",
                                                password='1234',
                                                is_active = True)


@pytest.fixture
def validation_token(user):
    token = ValidateUserTokenModel.objects.create(
        user=user,
        token=str(uuid.uuid4()),
        )
    return token

@pytest.fixture
def another_user():
    """Fixture for creating a test user who doesn't own the store"""
    return get_user_model().objects.create_user(email='test2@gmail.com',
                                                first_name = "konul",
                                                last_name = "bayramova",
                                                password='1234',
                                                is_active=True)


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
# a user that has already logged in
def another_authenticated_client(another_user):
    # get refresh token for the logged in user
    refresh=RefreshToken.for_user(another_user)
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


@pytest.fixture
def category():
    """Create a category for testing"""
    category = CategoryModel.objects.create(name="Test Category")
    return category


@pytest.fixture
def product(store, category):
    """Create a product for testing"""
    product = ProductModel.objects.create(
        name="Test Product",
        description="Product for testing images",
        price=10.00,
        stock=100,
        store=store,
    )
    product.categories.add(category)
    return product


@pytest.fixture(scope="function")
def image_file():
    """Create a sample image file for testing"""
    image = Image.new("RGB", (100, 100), color=(255, 0, 0))
    img_io = BytesIO()
    image.save(img_io, 'JPEG')
    img_io.seek(0)
    return InMemoryUploadedFile(img_io, None, 'test_image.jpg', 'image/jpeg', img_io.tell(), None)


@pytest.fixture
def product_data(store, category):
    image_file = BytesIO()
    image = Image.new('RGB', (100, 100), color=(73, 109, 137))
    image.save(image_file, format='JPEG')
    image_file.seek(0)

    image = SimpleUploadedFile("test_picture.jpg", image_file.read(), content_type="image/jpeg")
    return {
        "name": "New Test Product",
        "description": "Test Description",
        "price": 100,
        "stock": 10,
        "store": store.id,
        "categories": [category.id],
        "images": [image]
    }



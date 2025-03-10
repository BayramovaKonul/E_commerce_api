import pytest
from rest_framework.exceptions import ValidationError
from products.serializers import AddProductSerializer
from products.models import ProductModel, ProductImageModel
from store.models import StoreModel
from django.core.files.uploadedfile import SimpleUploadedFile
from ...confest import user, store, category, product, another_user, product_data
from rest_framework.test import APIRequestFactory
from django.urls import reverse
from rest_framework.request import Request
from rest_framework.parsers import MultiPartParser

@pytest.mark.django_db
class TestAddProductSerializer:

    # THIS TEST DOESNT WORK

    def test_add_product_with_valid_data(self, store, product_data):
        """Test adding a product with valid data"""

        factory = APIRequestFactory()
        url = reverse('add_product')  
        request = factory.post(url)  
        store = StoreModel.objects.get(id=product_data['store'])  # Fetch store instance
        request.user = store.owner  # Get the owner from the store

        serializer = AddProductSerializer(data=product_data, context={'request': request})
        assert serializer.is_valid(), f"Errors: {serializer.errors}"


        product = serializer.save()
   

        assert product.name == product_data["name"]
        assert product.description == product_data["description"]
        assert product.price == product_data["price"]
        assert product.stock == product_data["stock"]
        assert product.store.id == product_data["store"]
        assert list(product.categories.values_list('id', flat=True)) == product_data["categories"]
        assert product.images.exists(), "Product images were not saved."



    def test_invalid_store(self, user, another_user, store, category):
        """Test validation when the user is not the store owner"""

        factory = APIRequestFactory()
        url = reverse('add_product')

        data = {
            "name": "Test Product",
            "description": "Test Description",
            "price": 100,
            "stock": 10,
            "store": store.id,
            "categories": [category.id],
            "images": [],
        }

        # Create request and set user
        wsgi_request = factory.post(url, data, format='multipart')
        wsgi_request.user = another_user
        request = Request(wsgi_request) 

        serializer = AddProductSerializer(data=data, context={"request": request})

        with pytest.raises(ValidationError, match="You are not the owner of this store."):
            serializer.is_valid(raise_exception=True)


    def test_invalid_image_format(self, user, store, category):
        """Test adding product with an invalid image format"""

        invalid_file = SimpleUploadedFile("test.txt", b"file_content", content_type="text/plain")
        factory = APIRequestFactory()
        url = reverse('add_product')

        data = {
            "name": "Test Product",
            "description": "Test Description",
            "price": 100,
            "stock": 10,
            "store": store.id,
            "categories": [category.id],
            "images": [invalid_file],
        }

        wsgi_request = factory.post(url, data, format='multipart')
        wsgi_request.user = user
        request = Request(wsgi_request) 

        serializer = AddProductSerializer(data=data, context={"request": request})
        assert not serializer.is_valid()
        assert "images" in serializer.errors


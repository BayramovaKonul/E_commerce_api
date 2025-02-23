import pytest
from rest_framework.exceptions import ValidationError
from rest_framework.test import APIClient
from store.models import StoreModel
from store.serializers import CreateStoreSerializer
from ...confest import store, user, store_data
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APIRequestFactory
from django.urls import reverse

@pytest.mark.django_db
class TestCreateStoreSerializer:

    def test_create_store_with_valid_data(self, store_data):
        """Test creating a store with valid data"""
        factory = APIRequestFactory()
        url = reverse('create_store')  
        request = factory.post(url)  
        request.user = store_data['owner']  

        serializer = CreateStoreSerializer(data=store_data, context={'request': request})
        assert serializer.is_valid(), f"Errors: {serializer.errors}"


        store = serializer.save()
        
        assert store.name == store_data['name']
        assert store.description == store_data['description']
        assert store.address == store_data['address']
        assert store.website == store_data['website']
        assert store.picture.name.startswith('media/store_pictures/test_picture')
        assert store.owner == store_data['owner']
    

    def test_store_creation_invalid_image_format(self, store_data, user):
        """Test creating a store with an invalid image format"""

        factory = APIRequestFactory()
        url = reverse('create_store')  
        request = factory.post(url)  
        request.user = store_data['owner'] 

        store_data['picture'] = SimpleUploadedFile("invalid_picture.txt", b"file_content", content_type="text/plain")

        serializer = CreateStoreSerializer(data=store_data, context={'request': request})
        
        assert not serializer.is_valid()
        assert 'picture' in serializer.errors
        assert serializer.errors["picture"] == ["Upload a valid image. The file you uploaded was either not an image or a corrupted image."]
      

    def test_store_creation_exceeded_limit(self, store_data, user):
        """Test store creation when the owner already has 2 stores"""
        # Create two stores for the user
        factory = APIRequestFactory()
        url = reverse('create_store')  
        request = factory.post(url)  
        request.user = store_data['owner'] 

        StoreModel.objects.create(owner=user, name="Store 1", description="Desc 1", address="Address 1", website="https://store1.com")
        StoreModel.objects.create(owner=user, name="Store 2", description="Desc 2", address="Address 2", website="https://store2.com")
        
        serializer = CreateStoreSerializer(data=store_data, context={'request': request})
        
        assert not serializer.is_valid()
        assert 'owner' in serializer.errors
        assert serializer.errors["owner"] == ["You already have 2 stores. You cannot create more."]




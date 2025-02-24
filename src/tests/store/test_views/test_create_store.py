import pytest 
from django.urls import reverse
from rest_framework import status
from ...confest import authenticated_client, user, store_data, anonymous_client
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile


@pytest.mark.django_db
class TestCreateStoreView:

    def test_create_store_with_valid_credentials(self, authenticated_client, store_data):
        """Test that user create store with valid credentials """
        from django.utils.translation import activate
        activate('en')  # Ensures test runs in English without unwanted locale prefix

        url = reverse("create_store")


        res = authenticated_client.post(url, data=store_data, format='multipart')

        assert res.status_code == status.HTTP_201_CREATED
        assert res.data["message"] == "You created a new store successfully"


    def test_create_store_with_invalid_name(self, authenticated_client, store_data):
        """Test that user create a store with invalid name """

        url = reverse("create_store")

        store_data_invalid = store_data.copy()
        del store_data_invalid['name']

        res = authenticated_client.post(url, data=store_data_invalid, format='multipart')

        assert not res.status_code == status.HTTP_201_CREATED
        assert 'name' in res.data


    def test_create_store_with_invalid_picture(self, authenticated_client, store_data):
        """Test that user create a store with invalid picture"""

        url = reverse("create_store")

        store_data_invalid = store_data.copy()
        store_data_invalid['picture'] = SimpleUploadedFile("invalid_picture.txt", b"file_content", content_type="text/plain")

        res = authenticated_client.post(url, data=store_data_invalid, format='multipart')

        assert not res.status_code == status.HTTP_201_CREATED
        assert 'picture' in res.data


    def test_create_store_unauthenticated(self, anonymous_client, store_data):
        """Test creating a store without authentication."""

        url = reverse("create_store")
        response = anonymous_client.post(url, store_data, format='multipart')
        
        # Assert the response is a 401 Unauthorized
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
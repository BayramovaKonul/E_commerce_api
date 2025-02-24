import pytest
from django.urls import reverse
from rest_framework import status
from ...confest import authenticated_client, store, category, product_data, user, image_file, another_authenticated_client, another_user, anonymous_client

import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

@pytest.mark.django_db
class TestAddProductView:

    def test_add_product_with_valid_data(self, authenticated_client, product_data, image_file):
        """Test product creation with valid data"""

        from django.utils.translation import activate
        activate('en')  # Ensures test runs in English without unwanted locale prefix

        url = reverse('add_product')

        response = authenticated_client.post(url, data=product_data, format='multipart')
        print(response.data)

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["message"] == "You added a new product successfully"


    def test_add_product_with_invalid_data(self, authenticated_client, user):
        """Test product creation with invalid data"""

        url = reverse('add_product')

        invalid_data = {
            "name": "",  
            "price": -10,  
            "stock": "invalid", 
        }

        response = authenticated_client.post(url, data=invalid_data, format='multipart')

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "name" in response.data
        assert response.data["name"] == ["This field may not be blank."]
        assert "price" in response.data
        assert response.data["price"] == ["Ensure this value is greater than or equal to 0.01."]
        assert "stock" in response.data
        assert response.data["stock"] == ["A valid integer is required."]


    def test_add_product_when_user_is_not_store_owner(self, another_authenticated_client, product_data):
        """🚫 Test product creation when user is not the store owner"""

        url = reverse('add_product')

        response = another_authenticated_client.post(url, data=product_data, format='multipart')

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "store" in response.data
        assert response.data["store"] == ["You are not the owner of this store."]
 


    def test_add_product_unauthenticated(self, anonymous_client, product_data):
        """🔒 Test product creation without authentication"""
        url = reverse('add_product')

        response = anonymous_client.post(url, data=product_data, format='multipart')

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

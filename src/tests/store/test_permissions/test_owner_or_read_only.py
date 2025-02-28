import pytest
from rest_framework.test import APIClient
from rest_framework import status
from store.models import StoreModel
from django.contrib.auth.models import User
from ...confest import user, another_user, store, authenticated_client, another_authenticated_client
from django.urls import reverse

@pytest.mark.django_db
class TestIsStoreOwnerOrReadOnlyPermission:

    def test_store_owner_can_edit(self, store, authenticated_client):
        """Test that the store owner can edit their store"""

        url = reverse("update_store", kwargs={"store_id": store.id}) 

        # Perform a PATCH request (non-safe method)
        data = {'name': 'Updated Store Name'}
        response = authenticated_client.patch(url, data, format='multipart')

        assert response.status_code == status.HTTP_200_OK 
        assert response.data['name'] == 'Updated Store Name'


    def test_non_owner_cannot_edit(self, store, another_authenticated_client):
        """Test that a non-owner cannot edit the store"""
        
        url = reverse("update_store", kwargs={"store_id": store.id}) 

        # Perform a PATCH request (non-safe method)
        data = {'name': 'Updated Store Name'}
        response = another_authenticated_client.patch(url, data, format='multipart')

        assert response.status_code == status.HTTP_403_FORBIDDEN  


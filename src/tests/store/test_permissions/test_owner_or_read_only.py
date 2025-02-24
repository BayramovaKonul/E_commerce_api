import pytest
from rest_framework.test import APIClient
from rest_framework import status
from store.models import StoreModel
from django.contrib.auth.models import User
from ...confest import user, another_user, store
from django.urls import reverse

@pytest.mark.django_db
class TestIsStoreOwnerOrReadOnlyPermission:

    def test_store_owner_can_edit(self, store, user):
        """Test that the store owner can edit their store"""
        client = APIClient()
        client.force_authenticate(user=user)
        
        url = reverse("update_store", kwargs={"store_id": store.id}) 

        # Perform a PATCH request (non-safe method)
        data = {'name': 'Updated Store Name'}
        response = client.patch(url, data, format='multipart')

        assert response.status_code == status.HTTP_200_OK 
        assert response.data['name'] == 'Updated Store Name'


    def test_non_owner_cannot_edit(self, store, another_user):
        """Test that a non-owner cannot edit the store"""
        client = APIClient()

        client.force_authenticate(user=another_user)
        
        url = reverse("update_store", kwargs={"store_id": store.id}) 

        # Perform a PATCH request (non-safe method)
        data = {'name': 'Updated Store Name'}
        response = client.patch(url, data, format='multipart')

        assert response.status_code == status.HTTP_403_FORBIDDEN  # Non-owner should not be allowed



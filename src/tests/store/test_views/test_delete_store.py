import pytest
from rest_framework import status
from django.urls import reverse
from ...confest import authenticated_client, another_authenticated_client, user, another_user, product, store, category

@pytest.mark.django_db
class TestDeleteStoreView:
    
    def test_delete_store_success(self, authenticated_client, store):
        """Test deleting a store when the user is the owner"""

        url = reverse('delete_store', kwargs={'store_id': store.id})
        
        response = authenticated_client.delete(url)
        
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert response.data["message"] == "Store deleted successfully"


    def test_delete_store_not_owner(self, another_authenticated_client, store):
        """Test that a user who is not the owner cannot delete the store"""

        url = reverse('delete_store', kwargs={'store_id': store.id})
        
        response = another_authenticated_client.delete(url)
        
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.data["detail"] == "You do not have permission to perform this action."
        

    def test_delete_store_not_found(self, authenticated_client):
        """Test trying to delete a store that doesn't exist"""

        url = reverse('delete_store', kwargs={'store_id': 99999})  
        
        response = authenticated_client.delete(url)
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.data["detail"] == "No StoreModel matches the given query."

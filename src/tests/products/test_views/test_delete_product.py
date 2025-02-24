import pytest
from rest_framework import status
from django.urls import reverse
from ...confest import authenticated_client, another_authenticated_client, user, another_user, product, store, category

@pytest.mark.django_db
class TestDeleteProductView:
    
    def test_delete_product_success(self, authenticated_client, product):
        """Test deleting a product when the user is the owner"""

        url = reverse('delete_product', kwargs={'product_id': product.id})
        
        response = authenticated_client.delete(url)
        
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert response.data["message"] == "Product deleted successfully"


    def test_delete_product_not_owner(self, another_authenticated_client, product):
        """Test that a user who is not the owner cannot delete the product"""

        url = reverse('delete_product', kwargs={'product_id': product.id})
        
        response = another_authenticated_client.delete(url)
        
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.data["detail"] == "You do not have permission to perform this action."
        

    def test_delete_product_not_found(self, authenticated_client):
        """Test trying to delete a product that doesn't exist"""

        url = reverse('delete_product', kwargs={'product_id': 99999})  
        
        response = authenticated_client.delete(url)
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.data["detail"] == "No ProductModel matches the given query."

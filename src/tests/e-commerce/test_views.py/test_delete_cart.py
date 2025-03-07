import pytest
from rest_framework import status
from django.urls import reverse
from tests.confest import authenticated_client, another_authenticated_client, user, another_user, product, store, category
from e_commerce.models import CartModel

@pytest.mark.django_db
class TestDeleteFromCartView:
    
    def test_delete_cart_success(self, authenticated_client, product, user):
        """Test deleting a item from cart when the user is the owner"""

        cart = CartModel.objects.create(user=user, product=product)

        url = reverse('delete_cart', kwargs={'cart_id': cart.id})
        
        response = authenticated_client.delete(url)
        
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert response.data["message"] == "You removed the product from your cart successfully"


    def test_delete_cart_not_owner(self, another_authenticated_client, user, product):
        """Test that a user who is not the owner cannot delete the item from cart"""

        cart = CartModel.objects.create(user=user, product=product)
        url = reverse('delete_cart', kwargs={'cart_id': cart.id})
        
        response = another_authenticated_client.delete(url)
        
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.data["detail"] == "You do not have permission to perform this action."
        

    def test_delete_product_from_cart_not_found(self, authenticated_client):
        """Test trying to delete a product from cart that doesn't exist"""

        url = reverse('delete_cart', kwargs={'cart_id': 99999})  
        
        response = authenticated_client.delete(url)
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.data["detail"] == "No CartModel matches the given query."

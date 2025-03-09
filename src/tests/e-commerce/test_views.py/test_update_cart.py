import pytest
from rest_framework import status
from rest_framework.test import APIClient
from django.urls import reverse
from e_commerce.models import CartModel
from tests.confest import user, authenticated_client, product, cart_item, category, store, another_user, another_authenticated_client

@pytest.mark.django_db
class TestUpdateCartAPIView:

    def test_update_cart_valid_quantity(self, authenticated_client, cart_item):
        """Test updating a cart item with a valid quantity."""

        url = reverse('update_delete_cart', kwargs={'cart_id': cart_item.id})
        data = {'quantity': 3}

        response = authenticated_client.put(url, data, format="json")

        assert response.status_code == status.HTTP_200_OK

        # Check if the cart item quantity was updated in the database
        cart_item.refresh_from_db()
        assert cart_item.quantity == 3
        assert response.data["cart"][0]["quantity"] == 3


    def test_update_cart_invalid_quantity_zero(self, authenticated_client, cart_item):
        """Test updating a cart item with an invalid quantity (0)."""

        url = reverse('update_delete_cart', kwargs={'cart_id': cart_item.id})
        data = {'quantity': 0}

        response = authenticated_client.put(url, data, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST

        assert response.data == {'error': 'Invalid quantity. Quantity must be greater than 0.'}

        # Ensure the cart item was not updated in the database
        cart_item.refresh_from_db()
        assert cart_item.quantity != 0


    def test_update_cart_check_totals(self, authenticated_client, cart_item):
        """Test updating a cart item and checking that the cart totals are recalculated."""

        url = reverse('update_delete_cart', kwargs={'cart_id': cart_item.id})
        print(cart_item.id)
        data = {'quantity': 5}

        response = authenticated_client.put(url, data, format="json")

        assert response.status_code == status.HTTP_200_OK

        assert "cart_total" in response.data
        assert round(response.data['cart_total'], 2) > 0  

        cart_item.refresh_from_db()
        assert cart_item.quantity == 5


    def test_update_cart_not_owner(self, another_authenticated_client, cart_item):
        """Test that a user who is not the owner cannot update the item from cart"""
        
        url = reverse('update_delete_cart', kwargs={'cart_id': cart_item.id})
        print(cart_item.id)
        data = {'quantity': 5}
        
        response = another_authenticated_client.put(url, data, format="json")
        
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.data["detail"] == "You do not have permission to perform this action."


    def test_delete_cart_success(self, authenticated_client, product, user):
        """Test deleting a item from cart when the user is the owner"""

        cart = CartModel.objects.create(user=user, product=product)

        url = reverse('update_delete_cart', kwargs={'cart_id': cart.id})
        
        response = authenticated_client.delete(url)
        
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert response.data["message"] == "You removed the product from your cart successfully"


    def test_delete_cart_not_owner(self, another_authenticated_client, user, product):
        """Test that a user who is not the owner cannot delete the item from cart"""

        cart = CartModel.objects.create(user=user, product=product)
        url = reverse('update_delete_cart', kwargs={'cart_id': cart.id})
        
        response = another_authenticated_client.delete(url)
        
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.data["detail"] == "You do not have permission to perform this action."
        

    def test_delete_product_from_cart_not_found(self, authenticated_client):
        """Test trying to delete a product from cart that doesn't exist"""

        url = reverse('update_delete_cart', kwargs={'cart_id': 99999})  
        
        response = authenticated_client.delete(url)
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.data["detail"] == "No CartModel matches the given query."





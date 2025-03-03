import pytest
from rest_framework import status
from django.urls import reverse
from tests.confest import authenticated_client, another_authenticated_client, user, another_user, product, store, category
from e_commerce.models import WishlistModel

@pytest.mark.django_db
class TestDeleteWishlistView:
    
    def test_delete_wishlist_success(self, authenticated_client, product, user):
        """Test deleting a wislist when the user is the owner"""

        wishlist = WishlistModel.objects.create(user=user, product=product)

        url = reverse('delete_wishlist', kwargs={'id': wishlist.id})
        
        response = authenticated_client.delete(url)
        
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert response.data["message"] == "You removed the product from your wishlist successfully"


    def test_delete_wishlist_not_owner(self, another_authenticated_client, user, product):
        """Test that a user who is not the owner cannot delete the wishlist"""

        wishlist = WishlistModel.objects.create(user=user, product=product)
        url = reverse('delete_wishlist', kwargs={'id': wishlist.id})
        
        response = another_authenticated_client.delete(url)
        
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.data["detail"] == "You do not have permission to perform this action."
        

    def test_delete_product_from_wishlist_not_found(self, authenticated_client):
        """Test trying to delete a product from wishlist that doesn't exist"""

        url = reverse('delete_wishlist', kwargs={'id': 99999})  
        
        response = authenticated_client.delete(url)
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.data["detail"] == "No WishlistModel matches the given query."

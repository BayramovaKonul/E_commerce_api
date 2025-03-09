import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from e_commerce.models import CartModel, WishlistModel
from tests.confest import user, authenticated_client, product, store, product2, category, add_wishlist_items, add_comments


@pytest.mark.django_db
class TestMyCartView:

    def test_get_wishlist(self, authenticated_client, add_wishlist_items):
        """Test retrieving the authenticated user's wishlist."""
        url = reverse("list_add_wishlist")  
        response = authenticated_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2
        assert "average_rating" in response.data[0]


    def test_search_wishlist(self, authenticated_client, add_wishlist_items):
        """Test searching for a product in the wishlist."""
        url = reverse("list_add_wishlist") + "?search=Test Product 2"
        response = authenticated_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]["product"]["name"] == "Test Product 2"


    def test_wishlist_average_rating(self, authenticated_client, add_wishlist_items, add_comments):
        """Test if the wishlist correctly calculates the average rating."""
        url = reverse("list_add_wishlist")
        response = authenticated_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        # find wishlist items for "Test Product" and "Test Product 2"
        product_a = next(item for item in response.data if item["product"]["name"] == "Test Product")
        product_b = next(item for item in response.data if item["product"]["name"] == "Test Product 2")

        assert round(product_a["average_rating"] or 0, 2) == 4.5  # Handle None by defaulting to 0
        assert round(product_b["average_rating"] or 0, 2) == 3.0 


    def test_add_product_to_wishlist(self, authenticated_client, user, product):
        """Test that a product can be added to the wishlist."""
        
        url = reverse('list_add_wishlist')
        product_data={
            "product":product.id
        }
        response = authenticated_client.post(url, data=product_data)

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['message'] == "You added a product to wishlist"

        assert WishlistModel.objects.filter(user=user, product=product).exists()


    def test_add_duplicate_product_to_wishlist(self, authenticated_client, user, product):
        """Test that a duplicate product cannot be added to the wishlist."""

        WishlistModel.objects.create(user=user, product=product)

        url = reverse('list_add_wishlist')

        product_data={
            "product":product.id
        }

        response = authenticated_client.post(url, data=product_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert str(response.data['product'][0]) == "This product is already in your wishlist."

        assert WishlistModel.objects.filter(user=user, product=product).count() == 1


    def test_add_product_to_wishlist_invalid_product(self, authenticated_client, user):
        """Test that adding a non-existent product returns a 404 error."""

        url = reverse('list_add_wishlist')  

        product_data={
            "product":9999
        }
        response = authenticated_client.post(url, data=product_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
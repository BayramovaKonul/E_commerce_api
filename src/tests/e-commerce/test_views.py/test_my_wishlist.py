import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from e_commerce.models import CartModel
from tests.confest import user, authenticated_client, product, store, product2, category, add_wishlist_items, add_comments


@pytest.mark.django_db
class TestMyCartView:

    def test_get_wishlist(self, authenticated_client, add_wishlist_items):
        """Test retrieving the authenticated user's wishlist."""
        url = reverse("my_wishlist")  
        response = authenticated_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2
        assert "average_rating" in response.data[0]


    def test_search_wishlist(self, authenticated_client, add_wishlist_items):
        """Test searching for a product in the wishlist."""
        url = reverse("my_wishlist") + "?search=Test Product 2"
        response = authenticated_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]["product"]["name"] == "Test Product 2"


    def test_wishlist_average_rating(self, authenticated_client, add_wishlist_items, add_comments):
        """Test if the wishlist correctly calculates the average rating."""
        url = reverse("my_wishlist")
        response = authenticated_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        # find wishlist items for "Test Product" and "Test Product 2"
        product_a = next(item for item in response.data if item["product"]["name"] == "Test Product")
        product_b = next(item for item in response.data if item["product"]["name"] == "Test Product 2")

        assert round(product_a["average_rating"] or 0, 2) == 4.5  # Handle None by defaulting to 0
        assert round(product_b["average_rating"] or 0, 2) == 3.0 
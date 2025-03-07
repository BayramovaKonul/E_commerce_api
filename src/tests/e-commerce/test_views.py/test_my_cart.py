import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from e_commerce.models import CartModel
from tests.confest import user, authenticated_client, product, store, product2, cart_item, cart_item2, category


@pytest.mark.django_db
class TestMyCartView:

    def test_get_cart(self, authenticated_client, cart_item, cart_item2):
        """Test retrieving the authenticated user's cart."""
        url = reverse("my_cart")  
        response = authenticated_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert "cart" in response.data
        assert "sub_total" in response.data
        assert "cart_total" in response.data


    def test_search_cart(self, authenticated_client, cart_item, cart_item2):
        """Test searching for a product in the cart."""
        url = reverse("my_cart") + "?search=Test Product 2"
        response = authenticated_client.get(url)

        assert response.status_code == 200
        cart_products = response.data["cart"]
        assert len(cart_products) == 1
        assert response.data["cart"][0]["product"]["name"] == "Test Product 2"


    def test_cart_total_calculation(self, authenticated_client, cart_item, cart_item2):
        """Test if the cart total is calculated correctly."""
        url = reverse("my_cart")
        response = authenticated_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert round(response.data["sub_total"], 2) == 35.00  # (10*2) + (15*1)
        assert round(response.data["tax"], 2) == 3.50  # 10% tax
        assert round(response.data["cart_total"], 2) == 39.50  # subtotal + tax + shipping

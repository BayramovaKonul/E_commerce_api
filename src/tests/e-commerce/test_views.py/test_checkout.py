import pytest
from django.urls import reverse
from rest_framework import status
from unittest.mock import patch
from django.contrib.auth.models import User
from products.models import ProductModel
from account.models import AddressModel, UserProfileModel
from e_commerce.models import CartModel, OrderModel, OrderDetailsModel
from django.db import transaction
from tests.confest import order_detail, order, address, product, category, store, user, authenticated_client, cart_item
from django.core import mail

@pytest.mark.django_db
class TestCheckoutAPIView:

    @pytest.mark.django_db
    def test_checkout_empty_cart(self, authenticated_client):
        """Test the behavior when the cart is empty."""
        
        # Ensure the cart is empty
        CartModel.objects.all().delete()

        url = reverse('checkout')  
        response = authenticated_client.post(url)
        
        # Assert the status code and the expected error message
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "Your cart is empty. Please add items before checking out." in response.data["message"]


    @pytest.mark.django_db
    def test_checkout_create_order_without_default_address(self, authenticated_client, user, cart_item, address, order_detail):
        """Test creating an order without a default address."""
     
        url = reverse('checkout') 

        address_data = {
            "line1": "456 New St",
            "city": "New City",
            "country": "Newland",
            "is_default": True,
        }

        response = authenticated_client.post(url, address_data)

        # Ensure the address is created and order is created
        address = AddressModel.objects.first()
        assert address is not None
        assert address.user == user

        # Validate order is created with the new address
        order = OrderModel.objects.first()
        assert order.shipping_address == address


    
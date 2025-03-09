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
        assert "Your cart is empty. Please add items to your cart before checking out." in response.data["message"]


    @pytest.mark.django_db
    def test_checkout_create_order_with_default_address(self, authenticated_client, user, address, cart_item, order_detail):
        """Test creating an order when a default address exists."""

        address.is_default=True
        address.save()
        url = reverse('checkout')  
        
        # Ensure there's an order before the checkout
        assert not OrderModel.objects.count() == 0
        
        response = authenticated_client.post(url)

        # Validate order is created
        order = OrderModel.objects.first()
        assert response.status_code == status.HTTP_201_CREATED
        assert order.shipping_address == address
        assert OrderDetailsModel.objects.filter(order=order).count() == 1
        assert order.user == user
        assert "Thank you for your order. Please check your email for order details" in response.data["message"]

        # Verify stock is updated
        product = order_detail.product
        product.refresh_from_db()
        assert product.stock == 98  # 100 - 2 items purchased


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


    @pytest.mark.django_db
    def test_checkout_order_confirmation_email(self, authenticated_client, user, address, cart_item, order):
        """Test checking order confirmation email was sent"""

        address.is_default=True
        address.save()
        url = reverse('checkout')  
        response = authenticated_client.post(url)

        assert response.status_code == status.HTTP_201_CREATED

        assert len(mail.outbox) == 1  # Only one email should be in the outbox

        email = mail.outbox[0]
        
        order_number = OrderModel.objects.latest('id').id
        # Assert the email subject is correct
        assert email.subject.startswith("Order Confirmation - Order #")  # Check that it starts as expected
        assert f"Order #{order_number}" in email.subject 
        
        # Assert the email is sent to the correct address
        assert email.to == [user.email]
        
        # Check if the email body contains expected information
        assert f"Thank you for your order! Your order (Order #{order_number}) has been successfully placed." in email.body
        assert f"Order ID: {order_number}" in email.body
        




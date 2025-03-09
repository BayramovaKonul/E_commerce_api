import pytest
from django.urls import reverse
from rest_framework import status
from e_commerce.models.order import OrderModel
from products.models.product import ProductModel
from e_commerce.models import OrderDetailsModel
from tests.confest import user, order_detail, order, product, address, category, store

@pytest.mark.django_db
class TestOrderDetailsModel:
    def test_order_detail_creation(self, user, order_detail, order, product):
        """Test creating an order detail."""

        assert order_detail.order == order
        assert order_detail.product == product
        assert order_detail.quantity == 1
        assert order_detail.cost == 5.99
        assert order_detail.status == OrderDetailsModel.ProductStatus.PENDING


    def test_save_all_items_delivered_updates_order_status(self, order, product, order_detail):
        """Test that when all order details are delivered, the order status is updated."""
        
        order_detail.status='delivered'
        order_detail.save()  

        order.refresh_from_db()  
        assert order.status == OrderModel.OrderStatus.COMPLETED


    def test_save_some_items_not_delivered_does_not_update_order_status(self, order, order_detail, product):
        """Test that if not all items are delivered, order status is not updated."""
        order_detail.status='shipped'
        order_detail.save()  

        order.refresh_from_db()
        assert order.status == OrderModel.OrderStatus.PENDING

import pytest
from django.contrib.auth import get_user_model
from e_commerce.models import OrderDetailsModel, OrderModel
from products.models.product import ProductModel
from account.models.address import AddressModel
from tests.confest import user, order_detail, order, product, address, category, store

User = get_user_model()

@pytest.mark.django_db
class TestOrderModel:
    def test_order_creation(self, user, address, order):
        """Test creating an order."""
       
        assert order.user == user
        assert order.shipping_address == address
        assert order.status == OrderModel.OrderStatus.PENDING


    def test_order_status_change_to_completed(self, user, order, order_detail, address, product):
        """Test updating the order status when all order details are delivered."""

        order_detail.status='delivered'
        print(order_detail.status)
        order_detail.save()  
        order.refresh_from_db()
        assert order.status == OrderModel.OrderStatus.COMPLETED


    def test_order_status_remains_pending(self, order, order_detail, user, address, product):
        """Test order status remains 'pending' if not all items are delivered."""
        
        order_detail.status='packaged'
        order_detail.save()  
        order.refresh_from_db()
        assert order.status == OrderModel.OrderStatus.PENDING

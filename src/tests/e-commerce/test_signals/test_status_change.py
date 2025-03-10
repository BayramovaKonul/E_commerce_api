import pytest
from e_commerce.models import OrderModel, OrderDetailsModel
from tests.confest import user, order_detail, order, product, address, category, store

@pytest.mark.django_db
def test_signal_updates_order_status_when_all_items_delivered(order, order_detail):
    """Test that when all order details are marked as delivered, the order status updates to COMPLETED."""
    
    order_detail.status = OrderDetailsModel.ProductStatus.DELIVERED
    order_detail.save()  # trigger the signal

    order.refresh_from_db()  
    assert order.status == OrderModel.OrderStatus.COMPLETED


@pytest.mark.django_db
def test_signal_does_not_update_order_status_if_not_all_items_delivered(order, order_detail):
    """Test that if not all items are delivered, the order status does not update to COMPLETED."""
    
    order_detail.status = OrderDetailsModel.ProductStatus.SHIPPED
    order_detail.save()  

    order.refresh_from_db()
    assert order.status != OrderModel.OrderStatus.COMPLETED  

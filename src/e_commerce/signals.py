from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import OrderDetailsModel, OrderModel

@receiver(post_save, sender=OrderDetailsModel)
def update_order_status(sender, instance, **kwargs):
    """
    Signal to check if all items in an order are delivered.
    If so, update the order status to 'completed'.
    """
    order = instance.order  

    # If there are any order details that are not delivered
    if order.details.exclude(status=OrderDetailsModel.ProductStatus.DELIVERED).exists():
        return

    # If all order details are delivered, update the order status
    order.status = OrderModel.OrderStatus.COMPLETED
    order.save()

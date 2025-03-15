from django.db import transaction
from django.db.models import F
from .models import OrderModel, OrderDetailsModel
from products.models import ProductModel
from .utility import calculate_cart_totals
from account.tasks import send_order_confirmation_email
import logging

logger = logging.getLogger("base")

class CheckoutService:
    """
    Handles the checkout process: order creation, stock updates, cart clearing, and email notifications.
    """

    def __init__(self, user, cart_items, address):
        self.user = user
        self.cart_items = cart_items
        self.address = address
        self.order = None

    def process_order(self):
        """Main method to process the entire order."""
        with transaction.atomic():
            self._create_order()
            self._create_order_details()
            self._update_stock()
            self._clear_cart()
            self._send_confirmation_email()

        return self.order

    def _create_order(self):
        """Creates a new order for the user. (for internal use only since it is protected)"""
        self.order = OrderModel.objects.create(user=self.user, shipping_address=self.address)
        logger.info(f"Order created for user {self.user.id}, order ID: {self.order.id}")


    def _create_order_details(self):
        """Creates order details for each cart item."""
        order_details = [
            OrderDetailsModel(
                order=self.order,
                product=item.product,
                quantity=item.quantity,
                cost=item.product.price
            ) for item in self.cart_items
        ]
        OrderDetailsModel.objects.bulk_create(order_details)
        logger.info(f"{len(order_details)} order details created for order ID: {self.order.id}")


    def _update_stock(self):
        """Updates product stock based on purchased quantities."""
        products_to_update = []
        for item in self.cart_items:
            item.product.stock = F('stock') - item.quantity
            products_to_update.append(item.product)

        ProductModel.objects.bulk_update(products_to_update, ['stock'])
        logger.info(f"Product stock updated for {len(products_to_update)} products.")


    def _send_confirmation_email(self):
        """Sends an order confirmation email to the user."""
        serialized_order_details = [
            {
                'product_name': item.product.name,
                'quantity': item.quantity,
                'cost': item.cost,
                'product_id': item.product.id,
            } for item in self.order.details.all()
        ]
        
        cart_data = [{"item_total": item.product.price * item.quantity} for item in self.cart_items]
        totals = calculate_cart_totals(cart_data)

        send_order_confirmation_email.delay(
            self.user.email,
            self.user.id,
            self.order.id,
            serialized_order_details,
            totals,
            self.order.shipping_address.country
        )

        logger.info(f"Order confirmation email sent to user {self.user.email} with Order ID {self.order.id}")


    def _clear_cart(self):
        """Clears the user's cart after successful order placement."""
        self.cart_items.delete()
        logger.info(f"Cart items cleared for user {self.user.id}")

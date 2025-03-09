from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db import transaction
from django.utils.timezone import now
from django.contrib.auth.models import AnonymousUser
import logging
from ..utility import calculate_cart_totals
from ..serializers import CheckoutSerializer
from products.models import ProductModel
from ..models import CartModel, OrderModel, OrderDetailsModel
from account.models import AddressModel
from e_commerce.custom_permissions import IsOwnerOrReadOnly
from django.db.models import F
from account.tasks import send_order_confirmation_email

logger = logging.getLogger("base")


class CheckoutAPIView(APIView):
    permission_classes = [IsOwnerOrReadOnly]

    def post(self, request):
        """Handles checkout, creates an order, updates stock, and clears the cart."""

        default_address = AddressModel.objects.filter(user=request.user, is_default=True).first()
        cart_products=CartModel.objects.filter(user=request.user)

        if not cart_products:
            return Response({"message": "Your cart is empty. Please add items to your cart before checking out."}, status=status.HTTP_400_BAD_REQUEST)
    

        if not default_address:
            # No default address exists, validate the form for a new address
            serializer = CheckoutSerializer(data=request.data, context={"request": request})
            if serializer.is_valid():
                with transaction.atomic():
                    # Save address
                    address = serializer.save(user=request.user)
                    logger.info(f"Address saved for user {request.user.id}, address ID: {address.id}")

                    # Update default address
                    if serializer.validated_data.get('is_default'):
                        AddressModel.objects.filter(user=request.user, is_default=True).exclude(pk=address.pk).update(is_default=False)
                        logger.info(f"Set address {address.id} as default for user {request.user.id}")

                    # Proceed with order creation
                    order = self.create_order_and_process(request, address)
                    return Response({"message": "Thank you for your order. Please check your email for order details"}, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


        # If default address exists, use it directly to create the order without requiring a new address
        order = self.create_order_and_process(request, default_address)
        return Response({"message": "Thank you for your order. Please check your email for order details"}, status=status.HTTP_201_CREATED)


    def create_order_and_process(self, request, address):
        """Creates an order and processes cart details."""
        user = request.user
        # Create Order
        order = OrderModel.objects.create(user=user, shipping_address=address)
        logger.info(f"Order created for user {user.id}, order ID: {order.id}")

        # Fetch cart items for order details
        cart_items = CartModel.objects.filter(user=user)
        order_details = []
        products_to_update = []

        for item in cart_items:
            order_details.append(OrderDetailsModel(
                order=order,
                product=item.product,
                quantity=item.quantity,
                cost=item.product.price
            ))

            # Decrease stock in ProductModel
            item.product.stock = F('stock') - item.quantity
            products_to_update.append(item.product)

        # Bulk insert order details
        OrderDetailsModel.objects.bulk_create(order_details)
        logger.info(f"{len(order_details)} order details created for order ID: {order.id}")

        # Bulk update product stock
        ProductModel.objects.bulk_update(products_to_update, ['stock'])
        logger.info(f"Product stock updated for {len(products_to_update)} products.")

        # Calculate final amounts using the given function
        cart_data = [{"item_total": item.product.price * item.quantity} for item in cart_items]
        totals = calculate_cart_totals(cart_data)

        # Clear user's cart
        cart_items.delete()
        logger.info(f"Cart items cleared for user {user.id}")

        # Serialize the order details to dictionaries (for sending in email)
        serialized_order_details = [
            {
                'product_name': detail.product.name,
                'quantity': detail.quantity,
                'cost': detail.cost,
                'product_id': detail.product.id,
            }
            for detail in order_details
        ]

        # Send confirmation email
        send_order_confirmation_email.delay(
            user.email,
            user.id,
            order.id,
            serialized_order_details,
            totals,
            order.shipping_address.country
        )

        logger.info(f"Order confirmation email sent to user {user.email} with Order ID {order.id}")

        return order

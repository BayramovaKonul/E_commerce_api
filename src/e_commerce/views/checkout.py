from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from e_commerce.models import CartModel, OrderModel
from account.models import AddressModel
from e_commerce.serializers import CheckoutSerializer
from e_commerce.services import CheckoutService
import logging
from rest_framework import serializers

logger = logging.getLogger("base")

class CheckoutAPIView(APIView):

    def post(self, request):
        user = request.user

        # Check if cart is empty
        cart_products = CartModel.objects.filter(user=user)
        if not cart_products.exists():
            return Response(
                {"message": "Your cart is empty. Please add items before checking out."},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = CheckoutSerializer(data=request.data, context={"request": request})
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Get the shipping address (either existing default or newly created)
        address = serializer.save()

        # Process the order
        checkout_service = CheckoutService(user, cart_products, address)
        order = checkout_service.process_order()

        return Response(
            {"message": "Thank you for your order. Please check your email for order details."},
            status=status.HTTP_201_CREATED
        )

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from e_commerce.models import CartModel, OrderModel
from account.models import AddressModel
from e_commerce.serializers import CheckoutSerializer
from e_commerce.services import CheckoutService
import logging

logger = logging.getLogger("base")

class CheckoutAPIView(APIView):

    def post(self, request):
        user = request.user
        cart_products = CartModel.objects.filter(user=user)

        if not cart_products:
            return Response({"message": "Your cart is empty. Please add items to your cart before checking out."},
                            status=status.HTTP_400_BAD_REQUEST)

        # Determine the shipping address
        address = self.get_shipping_address(request)
        if not address:  
            return Response(
                {"message": "No default address found. Please provide a valid shipping address."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Process the order
        checkout_service = CheckoutService(user, cart_products, address)
        order = checkout_service.process_order()

        return Response(
            {"message": "Thank you for your order. Please check your email for order details"},
            status=status.HTTP_201_CREATED
        )

    def get_shipping_address(self, request):
        """
        Determines which shipping address to use (new or default).
        """
        user = request.user
        default_address = AddressModel.objects.filter(user=user, is_default=True).first()
        new_address_data = request.data

        if new_address_data:
            serializer = CheckoutSerializer(data=new_address_data, context={"request": request})
            if serializer.is_valid():
                with transaction.atomic():
                    address = serializer.save(user=user)
                    if serializer.validated_data.get('is_default'):
                        AddressModel.objects.filter(user=user, is_default=True).exclude(pk=address.pk).update(is_default=False)
                    return address
            return None

        if default_address:
            return default_address

        return None

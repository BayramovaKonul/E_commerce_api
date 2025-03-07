from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from e_commerce.models import CartModel
from ..serializers import MyCartSerializer
from ..utility import calculate_cart_totals
from ..custom_permissions import IsOwnerOrReadOnly
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

class UpdateCartAPIView(APIView):
    permission_classes = [IsOwnerOrReadOnly]

    def get_object(self, cart_id):
        return get_object_or_404(CartModel, id=cart_id)
    
    @swagger_auto_schema(
        operation_description="Update the quantity of a product in the user's cart",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'quantity': openapi.Schema(type=openapi.TYPE_INTEGER, description="New quantity of the product in the cart")
            },
            required=['quantity']
        ),
        responses={
            200: openapi.Response(
                description="Cart updated successfully with the updated cart items and totals",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'cart': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=MyCartSerializer(),
                            description="Updated list of cart items"
                        ),
                        'total': openapi.Schema(
                            type=openapi.TYPE_NUMBER,
                            format=openapi.FORMAT_DECIMAL,
                            description="Total cost of items in the cart"
                        ),
                        'tax': openapi.Schema(
                            type=openapi.TYPE_NUMBER,
                            format=openapi.FORMAT_DECIMAL,
                            description="Calculated tax for the cart"
                        ),
                        'shipping': openapi.Schema(
                            type=openapi.TYPE_NUMBER,
                            format=openapi.FORMAT_DECIMAL,
                            description="Shipping cost"
                        ),
                    }
                )
            ),
            400: openapi.Response(
                description="Bad request, invalid quantity provided",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'error': openapi.Schema(type=openapi.TYPE_STRING, description="Error message")
                    }
                )
            ),
            404: openapi.Response(
                description="Cart item not found",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'error': openapi.Schema(type=openapi.TYPE_STRING, description="Error message")
                    }
                )
            )
        }
    )
    def put(self, request, cart_id):

        new_quantity = request.data.get('quantity')

        # Validate the new quantity
        if int(new_quantity) <= 0:
            return Response({'error': 'Invalid quantity. Quantity must be greater than 0.'}, status=status.HTTP_400_BAD_REQUEST)

        cart_item = self.get_object(cart_id)
        self.check_object_permissions(request, cart_item)

        # Update the quantity and save
        cart_item.quantity = int(new_quantity)
        cart_item.save()

        cart_items = CartModel.objects.filter(user=request.user)

        # Serialize the updated cart item and return the response
        serializer = MyCartSerializer(cart_items, many=True)
        cart_totals = calculate_cart_totals(serializer.data)

        response_data = {
                'cart': serializer.data,
                **cart_totals 
            }
        
        return Response(response_data)

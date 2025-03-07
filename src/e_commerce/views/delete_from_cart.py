from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from ..custom_permissions import IsOwnerOrReadOnly
from ..models import CartModel
from django.shortcuts import get_object_or_404

class DeleteFromCartView(APIView):
    permission_classes = [IsOwnerOrReadOnly]

    def get_object(self, cart_id):
        return get_object_or_404(CartModel, id=cart_id)
    
    @swagger_auto_schema(
        operation_summary="Delete a product from the cart",
        operation_description="Deletes a specific product from the user's cart if they are the owner.",
        responses={
            204: openapi.Response(
                description="Product successfully removed from cart",
                examples={"application/json": {"success": True, "message": "You removed the product from your cart successfully"}}
            ),
            403: openapi.Response(description="Permission denied"),
            404: openapi.Response(description="Cart item not found"),
        },
    )

    def delete(self, request, cart_id):
        cart = self.get_object(cart_id)
        self.check_object_permissions(request, cart) # explicitly called
        cart.delete()
        return Response(
            data={"success": True, "message": "You removed the product from your cart successfully"},
            status=status.HTTP_204_NO_CONTENT
        )
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from ..custom_permissions import IsOwnerOrReadOnly
from ..models import WishlistModel
from django.shortcuts import get_object_or_404

class DeleteWishlistView(APIView):
    permission_classes = [IsOwnerOrReadOnly]

    def get_object(self, wishlist_id):
        return get_object_or_404(WishlistModel, id=wishlist_id)
    
    @swagger_auto_schema(
        operation_summary="Delete a product from the wishlist",
        operation_description="Deletes a specific product from the user's wishlist if they are the owner.",
        responses={
            204: openapi.Response(
                description="Product successfully removed from wishlist",
                examples={"application/json": {"success": True, "message": "You removed the product from your wishlist successfully"}}
            ),
            403: openapi.Response(description="Permission denied"),
            404: openapi.Response(description="Cart item not found"),
        },
    )

    def delete(self, request, wishlist_id):
        wishlist = self.get_object(wishlist_id)
        self.check_object_permissions(request, wishlist) # explicitly called
        wishlist.delete()
        return Response(
            data={"success": True, "message": "You removed the product from your wishlist successfully"},
            status=status.HTTP_204_NO_CONTENT
        )
from ..serializers import AddProductSerializer
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from ..custom_permissions import IsProductOwnerOrReadOnly
from ..models import ProductModel
from django.shortcuts import get_object_or_404
from drf_yasg import openapi

class DeleteProductView(APIView):
    permission_classes = [IsProductOwnerOrReadOnly]

    def get_object(self, product_id):
        return get_object_or_404(ProductModel, id=product_id)
    
    @swagger_auto_schema(
        operation_summary="Delete a product from a store",
        operation_description="Deletes a specific product from the user's store if they are the owner.",
        responses={
            204: openapi.Response(
                description="Product successfully removed from store",
                examples={"application/json": {"success": True, "message": "Product deleted successfully"}}
            ),
            403: openapi.Response(description="Permission denied"),
            404: openapi.Response(description="Product not found"),
        },
    )

    def delete(self, request, product_id):
        product = self.get_object(product_id)
        self.check_object_permissions(request, product) # explicitly called
        product.delete()
        return Response(
            data={"success": True, "message": "Product deleted successfully"},
            status=status.HTTP_204_NO_CONTENT
        )
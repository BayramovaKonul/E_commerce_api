from ..serializers import AddProductSerializer
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from ..custom_permissions import IsProductOwnerOrReadOnly
from ..models import ProductModel
from django.shortcuts import get_object_or_404

class DeleteProductView(APIView):
    permission_classes = [IsProductOwnerOrReadOnly]

    def get_object(self, product_id):
        return get_object_or_404(ProductModel, id=product_id)
    
    def delete(self, request, product_id):
        product = self.get_object(product_id)
        self.check_object_permissions(request, product) # explicitly called
        product.delete()
        return Response(
            data={"success": True, "message": "Product deleted successfully"},
            status=status.HTTP_204_NO_CONTENT
        )
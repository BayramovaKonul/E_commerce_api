from ..serializers import UpdateProductSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from ..models import ProductModel
from django.shortcuts import get_object_or_404
from ..custom_permissions import IsProductOwnerOrReadOnly

class UpdateProductView(APIView):
    permission_classes = [IsProductOwnerOrReadOnly]
    @swagger_auto_schema(
        request_body=UpdateProductSerializer,
        responses={
            200: UpdateProductSerializer,
            400: 'Bad request, invalid data.',
        }
    )
    def patch(self, request, product_id):
        product = get_object_or_404(ProductModel, id=product_id)
        self.check_object_permissions(request, product)

        serializer= UpdateProductSerializer(data=request.data, context = {'request':request}, 
                                          instance=product, partial=True)
        
        if serializer.is_valid(raise_exception=True):
            serializer.save(owner=request.user)
            return Response(
                {"message": "You updated your product details successfully", **serializer.data},
                status=status.HTTP_200_OK
            )

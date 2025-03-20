from ..serializers import UpdateProductSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from ..models import ProductModel
from django.shortcuts import get_object_or_404
from ..custom_permissions import IsProductOwnerOrReadOnly
from rest_framework.parsers import MultiPartParser, FormParser
from drf_yasg import openapi

class UpdateProductView(APIView):
    parser_classes = (MultiPartParser, FormParser)  # Required for file uploads
    permission_classes = [IsProductOwnerOrReadOnly]
    @swagger_auto_schema(
        request_body=UpdateProductSerializer,
        manual_parameters=[
            openapi.Parameter(
                'picture',
                openapi.IN_FORM,
                description="Upload store picture",
                type=openapi.TYPE_FILE,
                required=True
            )
        ],
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
            serializer.save()
            return Response(
                {"message": "You updated your product details successfully", **serializer.data},
                status=status.HTTP_200_OK
            )

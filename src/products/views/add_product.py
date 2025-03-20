from ..serializers import AddProductSerializer
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from rest_framework.parsers import MultiPartParser, FormParser
from drf_yasg import openapi

class AddProductView(APIView):
    parser_classes = (MultiPartParser, FormParser)  # Required for file uploads
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('name', openapi.IN_FORM, description="Product name", type=openapi.TYPE_STRING, required=True),
            openapi.Parameter('description', openapi.IN_FORM, description="Product description", type=openapi.TYPE_STRING, required=True),
            openapi.Parameter('price', openapi.IN_FORM, description="Product price", type=openapi.TYPE_NUMBER, required=True),
            openapi.Parameter('stock', openapi.IN_FORM, description="Available stock", type=openapi.TYPE_INTEGER, required=True),
            openapi.Parameter('store', openapi.IN_FORM, description="Store ID", type=openapi.TYPE_INTEGER, required=True),
            openapi.Parameter('categories', openapi.IN_FORM, description="Category IDs", type=openapi.TYPE_ARRAY, items=openapi.Items(type=openapi.TYPE_INTEGER)),
            openapi.Parameter('images', openapi.IN_FORM, description="Upload product images", type=openapi.TYPE_FILE, required=True),
        ],
        responses={201: "Product created successfully", 400: "Bad request, invalid data."}
    )
    def post(self, request):
        serializer= AddProductSerializer(data=request.data, context = {'request':request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"message": "You added a new product successfully"}, 
                            status=status.HTTP_201_CREATED)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from store.pagination import ItemsPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django.db.models import Q
from drf_yasg.utils import swagger_auto_schema
from rest_framework.parsers import MultiPartParser, FormParser
from drf_yasg import openapi
from ..models import ProductModel
from ..serializers import ListProductsSerializers
from django.db.models import Avg


class ListProductsView(APIView):
    parser_classes = [MultiPartParser, FormParser]
    permission_classes=[IsAuthenticatedOrReadOnly]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "search",
                openapi.IN_QUERY,
                description="Filter stores by name or description (case-insensitive match).",
                type=openapi.TYPE_STRING,
                required=False,
            ),
            openapi.Parameter(
                "page",
                openapi.IN_QUERY,
                description="Specify the page number for pagination.",
                type=openapi.TYPE_INTEGER,
                required=False,
            ),
            openapi.Parameter(
                "page_size",
                openapi.IN_QUERY,
                description="Specify the number of items per page (max 100).",
                type=openapi.TYPE_INTEGER,
                required=False,
            ),
        ],
        responses={
            200: openapi.Response(
                description="A paginated list of products.",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "count": openapi.Schema(type=openapi.TYPE_INTEGER, description="Total number of stores."),
                        "next": openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_URI, description="URL for the next page."),
                        "previous": openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_URI, description="URL for the previous page."),
                        "results": openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(
                                type=openapi.TYPE_OBJECT,
                                properties={
                                    "id": openapi.Schema(type=openapi.TYPE_INTEGER, description="Product ID"),
                                    "store": openapi.Schema(type=openapi.TYPE_STRING, description="Store name"),
                                    "price": openapi.Schema(type=openapi.FORMAT_DECIMAL, description="Product Price"),
                                    "stock": openapi.Schema(type=openapi.FORMAT_INT32, description="Product Stock"),
                                    "description": openapi.Schema(type=openapi.TYPE_STRING, description="Product description"),
                                    "categories": openapi.Schema(type=openapi.FORMAT_INT32, description="Product Categories"),
                                },
                            ),
                            description="List of product objects."
                        ),
                    },
                ),
            ),
            400: openapi.Response(description="Bad Request"),
        }
    )
    def get(self, request):
        query_params = dict(request.query_params)
        search=query_params.get('search')
        products = ProductModel.objects.annotate(
                        average_rating=Avg('comments__rating', default=0)  # Calculate average rating
                        ).prefetch_related('images').select_related('store')
        
        # Search
        if search:
            products = products.filter(Q(name__icontains=search[0]) |
                                       Q(description__icontains=search[0])|
                                       Q(store__name__icontains=search))
    

        # Order
        order_option = request.GET.get('order', 'default')

        if order_option == 'latest':
            products = products.order_by('-created_at')  
        elif order_option == 'price_low_to_high':
            products = products.order_by('price')  
        elif order_option == 'price_high_to_low':
            products = products.order_by('-price')

        # Pagination
        paginator = ItemsPagination()
        paginated_products = paginator.paginate_queryset(products, request)

        serializers=ListProductsSerializers(paginated_products, many=True)
        return paginator.get_paginated_response(serializers.data)
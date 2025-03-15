from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django.db.models import Q
from drf_yasg.utils import swagger_auto_schema
from rest_framework.parsers import MultiPartParser, FormParser
from drf_yasg import openapi
from ..models import CartModel
from ..serializers import MyCartSerializer, AddToCartSerializer
from django.db.models import Avg, Q
from django.db.models import F, Sum
from ..utility import calculate_cart_totals

class MyCartView(APIView):

    @swagger_auto_schema(
    operation_description="Get the user's shopping cart with optional search",
    responses={
        200: openapi.Response(
            description="Cart details with totals",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'cart': openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={  
                                'product': openapi.Schema(type=openapi.TYPE_OBJECT, properties={
                                    'name': openapi.Schema(type=openapi.TYPE_STRING),
                                    'price': openapi.Schema(type=openapi.TYPE_NUMBER),
                                }),
                                'average_rating': openapi.Schema(type=openapi.TYPE_NUMBER),
                                'quantity': openapi.Schema(type=openapi.TYPE_INTEGER),
                                'item_total': openapi.Schema(type=openapi.TYPE_NUMBER),
                            },
                        ),
                        description="List of cart items"
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
        )
    },
    manual_parameters=[
        openapi.Parameter(
            'search', openapi.IN_QUERY, description="Search term for product or store name", type=openapi.TYPE_STRING
        )
    ]
)

    def get(self, request):
        query_params = dict(request.query_params)
        search = query_params.get('search', [''])[0] 
        print(search)
        my_cart = CartModel.objects.filter(user=request.user)

        # Search
        if search:
            my_cart = my_cart.filter(
                Q(product__name__icontains=search) |
                Q(product__store__name__icontains=search)
            )

        serializer = MyCartSerializer(my_cart, many=True)
        cart_totals = calculate_cart_totals(serializer.data)

        return Response({
            'cart': serializer.data,
            **cart_totals
        })

    @swagger_auto_schema(
        request_body=AddToCartSerializer,
        responses={
            201: AddToCartSerializer,
            400: 'Bad request, invalid data.',
        }
    )

    def post(self, request):
        serializer = AddToCartSerializer(data=request.data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user)
            return Response({"message": "You added a product to your cart"}, 
                            status=status.HTTP_201_CREATED)

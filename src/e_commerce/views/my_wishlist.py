from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django.db.models import Q
from drf_yasg.utils import swagger_auto_schema
from rest_framework.parsers import MultiPartParser, FormParser
from drf_yasg import openapi
from ..models import WishlistModel
from ..serializers import MyWishlistSerializer, AddWishlistSerializer
from django.db.models import Avg


class MyWishListView(APIView):
    permission_classes=[IsAuthenticatedOrReadOnly]
    @swagger_auto_schema(
    operation_description="Get the user's wishlist with optional search",
    responses={
        200: openapi.Response(
            description="List of products in the wishlist with average ratings",
            schema=openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        # Define the properties of your wishlist items here.
                        # For example:
                        'product_name': openapi.Schema(type=openapi.TYPE_STRING),
                        'product_id': openapi.Schema(type=openapi.TYPE_INTEGER),
                        'average_rating': openapi.Schema(type=openapi.TYPE_NUMBER),
                    },
                    description="Wishlist item with product details"
                )
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

        my_wishlist = WishlistModel.objects.filter(user=request.user).annotate(
            average_rating=Avg('product__comments__rating')  
        ).prefetch_related('product__images')
        
        # Search
        if search:
            my_wishlist = my_wishlist.filter(
                Q(product__name__icontains=search) |
                Q(product__store__name__icontains=search)
            )

        serializer = MyWishlistSerializer(my_wishlist, many=True)
        return Response(serializer.data)

    

    @swagger_auto_schema(
        request_body=AddWishlistSerializer,
        responses={
            201: AddWishlistSerializer,
            400: 'Bad request, invalid data.',
        }
    )
    
    def post(self, request):
        print("post is called")
        serializer = AddWishlistSerializer(data=request.data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user)
            return Response({"message": "You added a product to wishlist"}, 
                            status=status.HTTP_201_CREATED)
        

    
    

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django.db.models import Q
from drf_yasg.utils import swagger_auto_schema
from rest_framework.parsers import MultiPartParser, FormParser
from drf_yasg import openapi
from ..models import WishlistModel
from ..serializers import MyWishlistSerializer
from django.db.models import Avg


class MyWishListView(APIView):

    @swagger_auto_schema(
        operation_description="Get the user's wishlist with optional search",
        responses={
            200: openapi.Response(
                description="List of products in the wishlist with average ratings",
                schema=openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=MyWishlistSerializer(),
                    description="List of wishlist items with product details"
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
    
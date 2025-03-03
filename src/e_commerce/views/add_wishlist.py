from ..serializers import AddWishlistSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema

class AddWishlistView(APIView):

    @swagger_auto_schema(
        request_body=AddWishlistSerializer,
        responses={
            201: AddWishlistSerializer,
            400: 'Bad request, invalid data.',
        }
    )

    def post(self, request, product_id):
        serializer= AddWishlistSerializer(data={"product": product_id}, context = {'request':request})
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user)
            return Response({"message": "You added a product to wishlist"}, 
                            status=status.HTTP_201_CREATED)
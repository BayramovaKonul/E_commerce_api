from ..serializers import AddToCartSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema

class AddToCartView(APIView):

    @swagger_auto_schema(
        request_body=AddToCartSerializer,
        responses={
            201: AddToCartSerializer,
            400: 'Bad request, invalid data.',
        }
    )

    def post(self, request, product_id):
        serializer= AddToCartSerializer(data={"product": product_id}, context = {'request':request})
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user)
            return Response({"message": "You added a product to your cart"}, 
                            status=status.HTTP_201_CREATED)
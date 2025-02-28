from ..serializers import AddProductSerializer
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema

class AddProductView(APIView):

    @swagger_auto_schema(
        request_body=AddProductSerializer,
        responses={
            201: AddProductSerializer,
            400: 'Bad request, invalid data.',
        }
    )
    def post(self, request):
        serializer= AddProductSerializer(data=request.data, context = {'request':request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"message": "You added a new product successfully"}, 
                            status=status.HTTP_201_CREATED)
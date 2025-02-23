from ..serializers import CreateStoreSerializer
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema

class CreateStoreView(APIView):

    @swagger_auto_schema(
        request_body=CreateStoreSerializer,
        responses={
            201: CreateStoreSerializer,
            400: 'Bad request, invalid data.',
        }
    )
    def post(self, request):
        serializer= CreateStoreSerializer(data=request.data, context = {'request':request})
        if serializer.is_valid(raise_exception=True):
            serializer.save(owner=request.user)
            return Response({"message": "You created a new store successfully"}, 
                            status=status.HTTP_201_CREATED)
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
        request_body=AddProductSerializer,
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
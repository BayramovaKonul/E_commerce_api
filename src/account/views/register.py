from ..serializers import UserRegisterSerializer
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema

class RegisterUserView(APIView):
    permission_classes = [AllowAny]  # Allow access without authentication

    @swagger_auto_schema(
        request_body=UserRegisterSerializer,
        responses={
            201: UserRegisterSerializer,
            400: 'Bad request, invalid data.',
        }
    )
    def post(self, request):
        serializer= UserRegisterSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"message": "You registered successfully"}, 
                            status=status.HTTP_201_CREATED)
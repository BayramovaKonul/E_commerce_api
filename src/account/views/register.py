from ..serializers import UserRegisterSerializer, UserValidationSerializer
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from ..tasks import send_welcoming_email_to_new_users
from ..models import ValidateUserTokenModel
from django.utils.timezone import now

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
            user=serializer.save()
            token = ValidateUserTokenModel.objects.create(user=user, is_used=False)

            send_welcoming_email_to_new_users.delay(user.email)
            return Response({"message": "You registered successfully. Please check your email to validate.",
                             "token": str(token.token),}, 
                            status=status.HTTP_201_CREATED)
        

class ValidateEmailView(APIView):
    permission_classes = [AllowAny] 

    @swagger_auto_schema(
        request_body=UserValidationSerializer,
        responses={
            201: UserValidationSerializer,
            400: 'Bad request, invalid token.',
        }
    )

    def post(self, request):
        token = request.data.get('token')

        serializer = UserValidationSerializer(data={"token": token})

        if serializer.is_valid():
            validation_token = serializer.validated_data['token']
            validation_token.is_used = True
            validation_token.expired_at = now()
            validation_token.save()
            user = validation_token.user
            user.is_active = True
            user.save()

            return Response({"message": "Email validated successfully!"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
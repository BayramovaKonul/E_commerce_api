from django.shortcuts import render
from ..serializers import (RequestForgotPasswordSerializer, ForgotPasswordSerializer)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.contrib.auth import get_user_model
from ..tasks import send_password_reset_email
from ..models import ForgotPasswordTokenModel
from django.conf import settings

User= get_user_model()


class RequestForgotPasswordView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        request_body=RequestForgotPasswordSerializer,
        responses={
            200: 'Password reset email sent.',
            400: 'Bad request, invalid data.',
    }
    )

    def post(self, request):
        serializer = RequestForgotPasswordSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']

            # Create a new token for the user
            user = User.objects.get(email=email)
            token = ForgotPasswordTokenModel.objects.create(user=user, is_used=False)

            # Send password reset email 
            reset_link = f"{settings.RESET_PASSWORD_URL}?token={token.token}"
            send_password_reset_email(email, reset_link)

            return Response({"message": "Password reset email sent.",
                             "token": str(token.token),
                             }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class ConfirmForgotPasswordView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        request_body=ForgotPasswordSerializer,
        responses={
            200: 'Password has been reset successfully.',
            400: 'Bad request, invalid data.',
    }
    )
    def post(self, request, *args, **kwargs):
        token = request.data['token']

        reset_token = ForgotPasswordTokenModel.objects.filter(token=token, is_used=False).first()

        user = reset_token.user

        serializer = ForgotPasswordSerializer(data=request.data, context={'user': user})

        if serializer.is_valid():
            serializer.save()

            return Response({"message": "Password has been reset successfully."}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
from ..serializers import UserProfileSerializer
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema

class UpdateUserProfileView(APIView):
    @swagger_auto_schema(
        request_body=UserProfileSerializer,
        responses={
            200: UserProfileSerializer,
            400: 'Bad request, invalid data.',
        }
    )
    def patch(self, request):
        user_profile = request.user.profile
        # Initialize the serializer
        serializer = UserProfileSerializer(user_profile, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
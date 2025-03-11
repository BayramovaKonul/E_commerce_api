from ..serializers import CommentRatingSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from ..models import ProductModel
from django.shortcuts import get_object_or_404
from ..tasks import analyze_comment_and_rate

class CommentProductView(APIView):

    @swagger_auto_schema(
        request_body=CommentRatingSerializer,
        responses={
            201: CommentRatingSerializer,
            400: 'Bad request, invalid data.',
        }
    )
    def post(self, request, product_id):
        product = get_object_or_404(ProductModel, id=product_id)
        serializer= CommentRatingSerializer(data=request.data, context = {'request':request})
        
        if serializer.is_valid(raise_exception=True):
            review=serializer.save(product=product, user=request.user)
            # Trigger the Celery task to analyze and rate the comment
            analyze_comment_and_rate.delay(review.id)
            return Response(
                {"message": "Thanks for your comment", **serializer.data},
                status=status.HTTP_201_CREATED
            )

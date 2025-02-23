from ..serializers import UpdateStoreSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from ..models import StoreModel
from django.shortcuts import get_object_or_404
from ..custom_permissions import IsStoreOwnerOrReadOnly

class UpdateStoreView(APIView):
    permission_classes = [IsStoreOwnerOrReadOnly]
    @swagger_auto_schema(
        request_body=UpdateStoreSerializer,
        responses={
            200: UpdateStoreSerializer,
            400: 'Bad request, invalid data.',
        }
    )
    def patch(self, request, store_id):
        store = get_object_or_404(StoreModel, id=store_id)
        self.check_object_permissions(request, store)

        serializer= UpdateStoreSerializer(data=request.data, context = {'request':request}, 
                                          instance=store, partial=True)
        
        if serializer.is_valid(raise_exception=True):
            serializer.save(owner=request.user)
            return Response(
                {"message": "You updated your store details successfully", **serializer.data},
                status=status.HTTP_200_OK
            )

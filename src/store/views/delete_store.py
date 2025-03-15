from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from ..custom_permissions import IsStoreOwnerOrReadOnly
from ..models import StoreModel
from django.shortcuts import get_object_or_404
from drf_yasg import openapi

class DeleteStoreView(APIView):
    permission_classes = [IsStoreOwnerOrReadOnly]

    def get_object(self, store_id):
        return get_object_or_404(StoreModel, id=store_id)
    
    @swagger_auto_schema(
        operation_summary="Delete a store",
        operation_description="Deletes a specific store of the user",
        responses={
            204: openapi.Response(
                description="Store successfully removed",
                examples={"application/json": {"success": True, "message": "Store deleted successfully"}}
            ),
            403: openapi.Response(description="Permission denied"),
            404: openapi.Response(description="Store not found"),
        },
    )

    def delete(self, request, store_id):
        store = self.get_object(store_id)
        self.check_object_permissions(request, store) 
        store.delete()
        return Response(
            data={"success": True, "message": "Store deleted successfully"},
            status=status.HTTP_204_NO_CONTENT
        )
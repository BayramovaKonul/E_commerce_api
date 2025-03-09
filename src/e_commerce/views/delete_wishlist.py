from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from ..custom_permissions import IsWishlistOwnerOrReadOnly
from ..models import WishlistModel
from django.shortcuts import get_object_or_404

class DeleteWishlistView(APIView):
    permission_classes = [IsWishlistOwnerOrReadOnly]

    def get_object(self, id):
        return get_object_or_404(WishlistModel, id=id)
    
    def delete(self, request, id):
        wishlist = self.get_object(id)
        self.check_object_permissions(request, wishlist) # explicitly called
        wishlist.delete()
        return Response(
            data={"success": True, "message": "You removed the product from your wishlist successfully"},
            status=status.HTTP_204_NO_CONTENT
        )
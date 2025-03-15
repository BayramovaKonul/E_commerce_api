from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from ..models import OrderDetailsModel
from ..serializers import OrderDetailStatusSerializer
from ..custom_permissions import IsOrderItemStoreOwnerOrReadOnly

class OrderItemStatusView(APIView):
    permission_classes = [IsOrderItemStoreOwnerOrReadOnly]
    
    def get(self, request, order_detail_id):
        """Retrieve the current status of a specific product in an order."""
        order_detail = get_object_or_404(OrderDetailsModel, id=order_detail_id)
        self.check_object_permissions(request, order_detail)
        serializer = OrderDetailStatusSerializer(order_detail)
        return Response(serializer.data)


    def patch(self, request, order_detail_id):
        """Update the status of a specific product in an order."""
        order_detail = get_object_or_404(OrderDetailsModel, id=order_detail_id)
        self.check_object_permissions(request, order_detail)
        serializer = OrderDetailStatusSerializer(order_detail, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Order item status updated successfully", "data": serializer.data})
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

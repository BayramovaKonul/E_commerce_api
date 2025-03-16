from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Sum, Avg
from ..models import StoreModel
from e_commerce.models import OrderModel, OrderDetailsModel
from products.models import CommentModel
from ..serializers import StoreOrderHistorySerializer
from django.db.models import Sum, F
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from ..custom_permissions import IsStoreOwnerorNoAccessDashboard
from ..pagination import ItemsPagination

class StoreOrderHistoryView(APIView):
    permission_classes = [IsStoreOwnerorNoAccessDashboard]
    
    @swagger_auto_schema(
        operation_description="Retrieve order history for a store",
        responses={
            status.HTTP_200_OK: openapi.Response(
                description="Order history data",
                examples={
                    "application/json": {
                        "order_data": [
                            {
                                "order_id": 1,
                                "order_date": "2025-01-01T12:00:00Z",
                                "customer": "customer@example.com",
                                "order_status": "Completed",
                                "shipping_address": "123 Main St, City, Country",
                                "products": [
                                    {
                                        "name": "Product 1",
                                        "quantity": 2,
                                        "cost": 10.0,
                                        "total_cost": 20.0
                                    }
                                ]
                            }
                        ]
                    }
                }
            ),
            status.HTTP_404_NOT_FOUND: openapi.Response(
                description="Store not found",
                examples={"application/json": {"error": "Store not found"}}
            ),
            status.HTTP_403_FORBIDDEN: openapi.Response(
                description="Permission denied",
                examples={"application/json": {"detail": "You do not have permission to perform this action."}}
            )
        }
    )

    def get(self, request, store_id, *args, **kwargs):
        user=self.request.user
        store = StoreModel.objects.filter(id=store_id).first()

        if not store:
            return Response({"error": "Store not found"}, status=status.HTTP_404_NOT_FOUND)
        
        # Retrieve only orders related to the store
        self.check_object_permissions(request, store) 
        all_orders = OrderDetailsModel.objects.select_related('order').filter(product__store=store)

        order_data = []

        for item in all_orders:
            order_details_dict = {
                "order_id": item.order.id,  
                "order_date": item.order.created_at,  
                "customer": item.order.user.email,  
                "order_status": item.order.status,  
                "shipping_address": item.order.shipping_address,
                "products": [
                    {
                        "name": item.product.name,
                        "quantity": item.quantity,
                        "cost": item.cost,
                        "total_cost": item.quantity * item.cost
                    } 
                ]
            }
            order_data.append(order_details_dict)

        paginator = ItemsPagination()
        paginated_orders = paginator.paginate_queryset(order_data, request)

        # Serialize data
        serializer = StoreOrderHistorySerializer({"order_data": paginated_orders})
        return Response(serializer.data, status=status.HTTP_200_OK)
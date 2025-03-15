from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Sum, Avg
from ..models import StoreModel
from e_commerce.models import OrderModel, OrderDetailsModel
from products.models import CommentModel
from ..serializers import StoreDashboardSerializer
from django.db.models import Sum, F
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class StoreDashboardView(APIView):
    @swagger_auto_schema(
        operation_description="Retrieve store dashboard statistics including total products, customers, profit, comments, sold products, store rating, and order details.",
        manual_parameters=[
            openapi.Parameter(
                'store_id', openapi.IN_PATH,
                description="ID of the store to retrieve dashboard data",
                type=openapi.TYPE_INTEGER,
                required=True
            )
        ],
        responses={
            200: StoreDashboardSerializer,
            400: openapi.Response("Bad Request - Not the store owner"),
            404: openapi.Response("Not Found - Store does not exist"),
        }
    )
    def get(self, request, store_id, *args, **kwargs):

        user = self.request.user
        store = StoreModel.objects.filter(id=store_id).first()

        if not store:
            return Response({"error": "Store not found"}, status=status.HTTP_404_NOT_FOUND)

        if store.owner != user:
            return Response({"error": "You are not allowed to view the store dashboard. You are not the owner."}, status=status.HTTP_400_BAD_REQUEST)

        # Total product count in the store
        total_products = store.products.count()

        # Total number of customers who placed orders in the store
        total_customers = OrderModel.objects.filter(details__product__store=store).values('user').distinct().count()

        # Total profit from orders in the store
        total_profit = OrderDetailsModel.objects.filter(product__store=store).aggregate(Sum('cost'))['cost__sum'] or 0

        # Total number of comments for the store's products
        total_comments = CommentModel.objects.filter(product__store=store).count()

        # Total number of sold products in the store
        total_sold_products = OrderDetailsModel.objects.filter(product__store=store).aggregate(Sum('quantity'))['quantity__sum'] or 0

        # Calculate the average rating of products for this store
        store_rating = CommentModel.objects.filter(product__store=store).aggregate(Avg('rating'))['rating__avg'] or 0

        # All orders made from this store
        all_orders = OrderModel.objects.filter(details__product__store=store)

        order_data = []
        for order in all_orders:
            # The order details to include only products from this store
            order_details = order.details.filter(product__store=store)

            if not order_details:
                # Skip orders that don't contain products from this store
                continue

            order_details_dict = {
                "order_id": order.id,
                "order_date": order.created_at,  
                "customer_email": order.user.email, 
                "order_status": order.status, 
                "shipping_address": order.shipping_address,
                "products": [
                    {
                        "name": item.product.name,
                        "quantity": item.quantity,
                        "cost": item.cost,
                        "total_cost": item.quantity * item.cost
                    } for item in order_details
                ]
            }
            order_data.append(order_details_dict)

        data = {
            'total_products': total_products,
            'total_customers': total_customers,
            'total_profit': total_profit,
            'total_comments': total_comments,
            'total_sold_products': total_sold_products,
            'store_rating': round(store_rating, 1),
            'order_data': order_data
        }

        serializer = StoreDashboardSerializer(data)
        return Response(serializer.data, status=status.HTTP_200_OK)

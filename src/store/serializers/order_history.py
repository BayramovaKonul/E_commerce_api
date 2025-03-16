from rest_framework import serializers

class ProductDetailSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    quantity = serializers.IntegerField()
    cost = serializers.DecimalField(max_digits=10, decimal_places=2)
    total_cost = serializers.DecimalField(max_digits=10, decimal_places=2)

class OrderDetailSerializer(serializers.Serializer):
    order_id = serializers.IntegerField()
    order_date = serializers.DateTimeField()
    customer = serializers.EmailField()
    order_status = serializers.CharField(max_length=50)
    shipping_address = serializers.CharField(max_length=500)
    products = ProductDetailSerializer(many=True)

class StoreOrderHistorySerializer(serializers.Serializer):
    order_data = OrderDetailSerializer(many=True)


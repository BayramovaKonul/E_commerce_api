from rest_framework import serializers

class StoreDashboardSerializer(serializers.Serializer):
    total_products = serializers.IntegerField()
    total_customers = serializers.IntegerField()
    total_profit = serializers.DecimalField(max_digits=10, decimal_places=2)
    total_comments = serializers.IntegerField()
    total_sold_products = serializers.IntegerField()
    store_rating = serializers.FloatField()

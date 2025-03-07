from rest_framework import serializers
from ..models import CartModel
from products.models import ProductImageModel, ProductModel

class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductModel
        fields = ['name', 'price']

class MyCartSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    average_rating = serializers.FloatField(read_only=True)
    item_total = serializers.SerializerMethodField()

    class Meta:
        model = CartModel
        fields = ['product', 'average_rating', 'quantity', 'item_total']


    def get_item_total(self, obj):
        # Calculate item total 
        return obj.quantity * obj.product.price 

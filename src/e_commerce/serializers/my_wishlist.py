from rest_framework import serializers
from ..models import WishlistModel
from products.models import ProductImageModel, ProductModel

class ProductPictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImageModel
        fields = ['image']

class ProductSerializer(serializers.ModelSerializer):
    images = ProductPictureSerializer(many=True)

    class Meta:
        model = ProductModel
        fields = ['name', 'price', 'store', 'images']

class MyWishlistSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    average_rating = serializers.FloatField(read_only=True)

    class Meta:
        model = WishlistModel
        fields = ['product', 'average_rating']

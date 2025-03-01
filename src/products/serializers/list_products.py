from rest_framework import serializers
from ..models import ProductModel, ProductImageModel
from store.models import StoreModel
from account.serializers import UserBaseSerializer
from django.core.exceptions import ValidationError

class ProductPictureSerializer(serializers.ModelSerializer):
    class Meta:
        model=ProductImageModel
        fields=['image']

        
class ListProductsSerializers(serializers.ModelSerializer):
    images = ProductPictureSerializer(many=True)

    class Meta:
        model=ProductModel
        fields=['name', 'description', 'store', 'images', 'price', 'stock', 'categories']
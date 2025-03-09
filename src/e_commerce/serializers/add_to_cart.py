from rest_framework import serializers
from ..models import CartModel
from account.serializers import UserBaseSerializer
import mimetypes
from django.core.exceptions import ValidationError

class AddToCartSerializer(serializers.ModelSerializer):

    class Meta:
        model = CartModel
        fields = ['product']

    def validate(self, data):
        user = self.context['request'].user 
        product = data.get('product') 

        if CartModel.objects.filter(user=user, product=product).exists():
            raise serializers.ValidationError(
                {"product": ["This product is already in your cart."]}
            )
        return data
    
    def create(self, validated_data):
        user = self.context['request'].user
        product = validated_data['product']

        cart_item = CartModel.objects.create(user=user, product=product)
        return cart_item
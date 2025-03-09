from rest_framework import serializers
from ..models import WishlistModel
from account.serializers import UserBaseSerializer
import mimetypes
from django.core.exceptions import ValidationError

class AddWishlistSerializer(serializers.ModelSerializer):

    class Meta:
        model = WishlistModel
        fields = ['product']

    def validate(self, data):
        user = self.context['request'].user 
        product = data.get('product') 

        if WishlistModel.objects.filter(user=user, product=product).exists():
            raise serializers.ValidationError(
                {"product": ["This product is already in your wishlist."]}
            )
        return data
    
    def create(self, validated_data):
        user = self.context['request'].user
        product = validated_data['product']

        # Explicitly pass the user when creating the WishlistModel
        wishlist_item = WishlistModel.objects.create(user=user, product=product)
        return wishlist_item
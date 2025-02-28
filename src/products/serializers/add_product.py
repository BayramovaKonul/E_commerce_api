from rest_framework import serializers
from ..models import ProductModel, ProductImageModel
from account.serializers import UserBaseSerializer
import mimetypes
from django.core.exceptions import ValidationError

class AddProductSerializer(serializers.ModelSerializer):
    images = serializers.ListField(
        child=serializers.ImageField(max_length=None, allow_empty_file=False, use_url=False),
        write_only=True
    )

    class Meta:
        model = ProductModel
        fields = ['name', 'description', 'price', 'stock', 'store', 'categories', 'images']


    def validate_store(self, store):
        """
        Ensure that the store belongs to the current user (store owner).
        """
        user = self.context.get('request').user 

        if store.owner != user: 
            raise serializers.ValidationError("You are not the owner of this store.")
        return store
    

    def validate_images(self, images):
        """
        Validate that all uploaded files are valid images.
        """
        for image in images:
            if not image.content_type.startswith('image/'):
                raise serializers.ValidationError(f"{image.name} is not a valid image file.")
        return images
    

    def create(self, validated_data):
        images = validated_data.pop('images', [])
        # because of many-to-many relationship we can't directly assign
        categories = validated_data.pop('categories', [])
        product = ProductModel.objects.create(**validated_data)

        product.categories.set(categories)

        for image in images:
            ProductImageModel.objects.create(product=product, image=image)

        return product



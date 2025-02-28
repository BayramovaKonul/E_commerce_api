from rest_framework import serializers
from .add_product import AddProductSerializer
from ..models import ProductImageModel

class UpdateProductSerializer(AddProductSerializer):

    def update(self, instance, validated_data):
        images = validated_data.pop('images', None)
        categories = validated_data.pop('categories', None)

        # Update fields in the product model
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()

        # Update many-to-many relationship with categories
        if categories is not None:
            instance.categories.set(categories)

        # Handle image updates
        if images is not None:

            for image in images:
                ProductImageModel.objects.create(product=instance, image=image)

        instance.save()
        return instance

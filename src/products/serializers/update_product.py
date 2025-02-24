from rest_framework import serializers
from .add_product import AddProductSerializer
from ..models import ProductImageModel

class UpdateProductSerializer(AddProductSerializer):

    def update(self, instance, validated_data):
        images = validated_data.pop('images', None)

        # Handle image updates
        if images is not None:
            # Remove old images
            # instance.images.all().delete()  

            for image in images:
                ProductImageModel.objects.create(product=instance, image=image)

        instance.save()
        return instance

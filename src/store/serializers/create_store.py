from rest_framework import serializers
from ..models import StoreModel
from account.serializers import UserBaseSerializer
import mimetypes
from django.core.exceptions import ValidationError

class CreateStoreSerializer(serializers.ModelSerializer):

    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model=StoreModel
        fields=['name', 'description', 'address', 'website', 'picture', 'owner']


    def validate_owner(self, value):
        """
        Validates that the owner doesn't exceed the store limit.
        """
        store_count = StoreModel.objects.filter(owner=value).count()
        if store_count >= 2:
            raise ValidationError("You already have 2 stores. You cannot create more.")
        return value
        

    def validate_picture(self, value):
        """
        Validate the picture's MIME type or size 
        """
        if value:
            mime_type, _ = mimetypes.guess_type(value.name)
            if mime_type not in ['image/jpeg', 'image/png']:
                raise ValidationError("Only JPEG and PNG image formats are allowed.")
        return value
        
        
    def create(self, validated_data):
        """
        Set the owner to request.user automatically.
        """
        # Set the owner to request.user
        request = self.context.get('request')
        if request and request.user:
            validated_data['owner'] = request.user

        return super().create(validated_data)
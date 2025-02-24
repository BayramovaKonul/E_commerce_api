from rest_framework import serializers
from ..models import StoreModel
from account.serializers import UserBaseSerializer
from django.core.exceptions import ValidationError

class ListStoreSerializers(serializers.ModelSerializer):
    owner = UserBaseSerializer()
    class Meta:
        model=StoreModel
        fields=['owner', 'name', 'description', 'address', 'website', 'picture', 'created_at']
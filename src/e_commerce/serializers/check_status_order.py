from rest_framework import serializers
from ..models import OrderDetailsModel

class OrderDetailStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderDetailsModel
        fields = ['status']

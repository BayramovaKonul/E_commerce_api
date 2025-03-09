from rest_framework import serializers
from account.models import AddressModel
from django.core.exceptions import ValidationError

class CheckoutSerializer(serializers.ModelSerializer):

    class Meta:
        model = AddressModel
        fields = ['address', 'country', 'city', 'zip_code', 'is_default']
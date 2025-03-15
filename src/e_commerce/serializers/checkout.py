from rest_framework import serializers
from account.models import AddressModel
from django.core.exceptions import ValidationError
from django.db import transaction
class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = AddressModel
        fields = ['address', 'country', 'city', 'zip_code', 'is_default']

class CheckoutSerializer(serializers.Serializer):
    use_default_address = serializers.BooleanField()
    address_data = AddressSerializer(required=False, allow_null=True)

    def validate(self, data):
        use_default_address = data.get("use_default_address")
        address_data = data.get("address_data")

        if not use_default_address and address_data is None:
            raise serializers.ValidationError(
                {"address_data": "This field is required when use_default_address is False."}
            )

        return data
    
    def create(self, validated_data):
        """Handles address creation if a new address is provided."""
        user = self.context["request"].user
        use_default_address = validated_data.get("use_default_address")
        
        with transaction.atomic():
            if use_default_address:
                default_address = AddressModel.objects.filter(user=user, is_default=True).first()
                if not default_address:
                    raise serializers.ValidationError("No default address found. Please provide a new address.")
                return default_address
            
            # Create new address and assign user
            address_data = validated_data.get("address_data")

            if address_data:
                address = AddressModel.objects.create(user=user, **address_data)

                # If the new address is marked as default, update other addresses
                if address.is_default:
                    AddressModel.objects.filter(user=user, is_default=True).exclude(pk=address.pk).update(is_default=False)

                return address
            
            raise serializers.ValidationError("No address provided.")
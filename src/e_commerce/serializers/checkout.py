from rest_framework import serializers
from account.models import AddressModel
from django.core.exceptions import ValidationError

class CheckoutSerializer(serializers.ModelSerializer):
    use_default_address = serializers.BooleanField(required=False, default=False)
    
    class Meta:
        model = AddressModel
        fields = ['use_default_address', 'address', 'country', 'city', 'zip_code', 'is_default']
    
    def to_internal_value(self, data):
        """Ensures that either a default address is used or a new address is provided."""
        user = self.context["request"].user
        use_default = data.get("use_default_address", False)
        
        if use_default:
            default_address = AddressModel.objects.filter(user=user, is_default=True).first()
            if not default_address:
                raise serializers.ValidationError("No default address found. Please provide a new address.")
            
            # in case to update current default address only if user provides a field)
            merged_data = {
                "use_default_address": True,
                "address": data.get("address", default_address.address),
                "country": data.get("country", default_address.country),
                "city": data.get("city", default_address.city),
                "zip_code": data.get("zip_code", default_address.zip_code),
            }
            # Store default address for later use (create method)
            self.default_address = default_address
            return super().to_internal_value(merged_data) 

        return super().to_internal_value(data)
    
    def create(self, validated_data):
        """Creates a new address or uses the default if none provided."""
        user = self.context["request"].user

        # If default address was selected, return it
        if hasattr(self, 'default_address'):
            # Update existing default address instead of creating a new one
            for key, value in validated_data.items():
                setattr(self.default_address, key, value)
            self.default_address.save()
            return self.default_address

        # Otherwise, create a new address
        validated_data.pop("use_default_address", None)
        address = AddressModel.objects.create(user=user, **validated_data)

        return address

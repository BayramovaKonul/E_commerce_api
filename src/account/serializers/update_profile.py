from rest_framework import serializers
from ..models import CustomUserModel, UserProfileModel
from rest_framework.validators import ValidationError
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from django.contrib.auth import get_user_model
import re
import logging

logger=logging.getLogger("base")

class UserProfileSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source='user.first_name', required=False)
    last_name = serializers.CharField(source='user.last_name', required=False)

    class Meta:
        model= UserProfileModel
        fields =['birthday', 'phone_number', 'first_name', 'last_name']

    
    def validate_phone_number(self, value):
        """Validates and normalizes Azerbaijani phone numbers."""

        if value is None or value == "":  # If phone number is empty or None, 
            return self.instance.phone_number  # Keep the existing phone number in the profile
        
        print("fqerfr4gfr", self.instance.phone_number)
        
        original_value = value.strip().replace(" ", "") 

        patterns = [
            r"^\+994(50|51|55|70|77|99)\d{7}$",  # Format: +994XXXXXXXXX
            r"^0(50|51|55|70|77|99)\d{7}$",      # Format: 05XXXXXXXX
            r"^(50|51|55|70|77|99)\d{7}$"        # Format: 5XXXXXXXX
        ]

        if any(re.match(pattern, original_value) for pattern in patterns):
            if original_value.startswith("0"):  
                normalized_number = "+994" + original_value[1:]  # Convert `055XXXXXXX` → `+99455XXXXXXX`
            elif not original_value.startswith("+994"):  
                normalized_number = "+994" + original_value  # Convert `558888888` → `+994558888888`
            else:
                normalized_number = original_value

            logger.info(f"Phone number validated and normalized: {normalized_number}")
            return normalized_number  
        
            
        logger.warning(f"Invalid phone number format attempted: {original_value}")
        raise serializers.ValidationError("Invalid phone number format. Use +994XXXXXXXXX, 05XXXXXXXX, or 5XXXXXXXX.")
    

    def update(self, instance, validated_data):
        # Extract user data from validated_data
        logger.info(f"Starting update for UserProfile ID {instance.id} - User ID {instance.user.id}")
        
        user_data = {}
        if 'first_name' in validated_data:
            user_data['first_name'] = validated_data.pop('first_name')
        if 'last_name' in validated_data:
            user_data['last_name'] = validated_data.pop('last_name')

        user_data = validated_data.pop('user', {})

        logger.debug(f"Extracted user data: {user_data}")
        logger.debug(f"Extracted profile data: {validated_data}")

        # Update UserProfileModel
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        logger.info(f"Updated UserProfile ID {instance.id} with data: {validated_data}")

        # Update CustomUserModel
        user = instance.user
        for attr, value in user_data.items():
            setattr(user, attr, value)
        user.save()
        logger.info(f"Updated CustomUser ID {user.id} with data: {user_data}")

        return instance

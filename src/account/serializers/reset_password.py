from rest_framework import serializers
from django.contrib.auth.hashers import check_password

class ResetPasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True, min_length=8)
    confirm_password = serializers.CharField(required=True, write_only=True)

    def validate_old_password(self, value):
        user = self.context.get('user')

        if not check_password(value, user.password):
            raise serializers.ValidationError("The old password is incorrect.")
        return value

    def validate(self, data):
        new_password = data.get('new_password')
        confirm_password = data.get('confirm_password')

        if new_password != confirm_password:
            raise serializers.ValidationError({"confirm_password": "Passwords do not match."})
        return data

    def save(self, **kwargs):
        user = self.context.get('user') 
        user.set_password(self.validated_data['new_password'])
        user.save()
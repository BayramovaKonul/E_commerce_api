from rest_framework import serializers
from ..models import CustomUserModel, UserProfileModel
# from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from rest_framework.validators import ValidationError
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

User= get_user_model()

class UserBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUserModel
        fields = ['email', 'first_name', 'last_name']

class UserRegisterSerializer(serializers.ModelSerializer):
    # use them when writing data to the database, but don't include in response
    password1 = serializers.CharField(write_only=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUserModel
        fields = ['first_name', 'last_name', 'email', 'password1', 'password2']


    def validate_email(self, email):
        if CustomUserModel.objects.filter(email=email).exists():
            raise serializers.ValidationError("This email is already registered.")  
        return email
        

    def validate(self, data):
        password1 = data.get('password1')
        password2 = data.get('password2')

        if password1 != password2:
            raise serializers.ValidationError({"password2": "Passwords must match."})

        return data
    
    def create(self, validated_data):
        validated_data.pop('password2') 
        validated_data['password'] = make_password(validated_data.pop('password1'))  
        return CustomUserModel.objects.create(**validated_data)
     
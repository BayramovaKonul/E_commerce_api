from rest_framework import serializers
from ..models import CustomUserModel, UserProfileModel
# from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from rest_framework.validators import ValidationError
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from ..utility import generate_token
from ..tasks import validate_new_user_email
from ..models import ValidateUserTokenModel

User= get_user_model()


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

        user = CustomUserModel.objects.create(**validated_data)
        token = generate_token(user)

        validate_new_user_email.delay(user.email, token)

        return user
    

class UserValidationSerializer(serializers.Serializer):
    token = serializers.CharField()

    def validate_token(self, token):

        token_obj = ValidateUserTokenModel.objects.filter(token=token, is_used=False).first()
        if not token_obj or token_obj.is_expired():
            raise serializers.ValidationError({"Invalid or expired token."})
        
        return token_obj

     
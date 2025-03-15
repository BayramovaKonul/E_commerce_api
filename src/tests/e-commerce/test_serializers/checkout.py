import pytest
from rest_framework.exceptions import ValidationError
from rest_framework.test import APIRequestFactory
from account.models import AddressModel
from e_commerce.serializers import CheckoutSerializer
from django.contrib.auth.models import User
from tests.confest import user, address

@pytest.mark.django_db
class TestCheckoutSerializer:

    def test_checkout_with_default_address(self, address, user):
        """Test using a default address."""
        address['is_default']=True
        address.save()

        data= {
            'use_default_address':True
        }

        factory = APIRequestFactory()
        request = factory.post('/checkout/', data)
        request.user = user

        serializer = CheckoutSerializer(data=data, context={'request': request})
        
        # Simulate fetching the default address from the database.
        serializer.is_valid(raise_exception=True)
        
        assert serializer.validated_data["address"] == address.address
        assert serializer.validated_data["country"] == address.country
        assert serializer.validated_data["city"] == address.city
        assert serializer.validated_data["zip_code"] == address.zip_code
    

    def test_checkout_with_no_default_address(self, address, user):
        """Test that an exception is raised when no default address is available."""

        address_data={
            "use_default_address": True,
            "address": "456 Another St",
            "country": "Test Country",
            "city": "Test City",
            "zip_code": "67890"
        }

        factory = APIRequestFactory()
        request = factory.post('/checkout/', address_data)
        request.user = user

        serializer = CheckoutSerializer(data=address_data, context={'request': request})

        with pytest.raises(ValidationError):
            serializer.is_valid(raise_exception=True)


    def test_create_with_default_address(self, address, user):
        """Test updating an existing default address when 'use_default_address' is true."""
        address['is_default']=True
        address.save()

        data= {
            'country':'England',
            'use_default_address':True
        }

        factory = APIRequestFactory()
        request = factory.post('/checkout/', data)
        request.user = user

        serializer = CheckoutSerializer(data=data, context={'request': request})

        # The default address should be updated
        serializer.is_valid(raise_exception=True)
        updated_address = serializer.save()

        assert updated_address.address == address["address"]
        assert updated_address.country == 'England'
        assert updated_address.city == address["city"]
        assert updated_address.zip_code == address["zip_code"]
    

    def test_create_with_new_address(self, address, user):
        """Test creating a new address if no default address is used."""

        address_data={
            "use_default_address": True,
            "address": "456 Another St",
            "country": "Test Country",
            "city": "Test City",
            "zip_code": "67890"
        }

        factory = APIRequestFactory()
        request = factory.post('/checkout/', address_data)
        request.user = user

        serializer = CheckoutSerializer(data=address_data, context={'request': request})

        serializer.is_valid(raise_exception=True)
        new_address = serializer.save()

        assert new_address.address == address_data["address"]
        assert new_address.country == address_data["country"]
        assert new_address.city == address_data["city"]
        assert new_address.zip_code == address_data["zip_code"]
        assert new_address.user == user


    def test_create_with_missing_address_field(self, checkout_data, address, user):
        """Test that an exception is raised when essential address fields are missing."""

        uncompleted_address_data={
            "use_default_address": True,
            "address": "456 Another St",
            "zip_code": "67890"
        }
        factory = APIRequestFactory()
        request = factory.post('/checkout/', uncompleted_address_data)
        request.user = user

        serializer = CheckoutSerializer(data=uncompleted_address_data, context={'request': request})

        with pytest.raises(ValidationError):
            serializer.is_valid(raise_exception=True)

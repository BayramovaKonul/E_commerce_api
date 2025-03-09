import pytest
from django.contrib.auth import get_user_model
from account.models import AddressModel
from tests.confest import user, order_detail, order, product, address, category, store

User = get_user_model()

@pytest.mark.django_db
class TestAddressModel:
    def test_address_creation(self, address, user):
        """Test creating an address."""

        assert address.user == user
        assert address.address == "Test address"
        assert address.country == "Test country"
        assert address.city == "Test city"
        assert address.zip_code == "Test zip code"
        assert address.is_default is False


    def test_multiple_addresses(self, user, address):
        """Test user having multiple addresses."""
     
        address2 = AddressModel.objects.create(
            user=user,
            address="Another St.",
            country="Another Country",
            city="Another City",
            zip_code="67890",
            is_default=True
        )

        assert address.is_default is False
        assert address2.is_default is True

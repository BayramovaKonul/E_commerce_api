import pytest
from store.models import StoreModel
from ...confest import store, user
from django.core.exceptions import ValidationError

@pytest.mark.django_db
class TestStoreModel:
    
    def test_create_store(self, store):
        '''Test creating a store with valid credentials'''
        assert store.name == 'Test Store'
        assert store.description == 'This is a test store.'
        assert store.address == '123 Test Street'
        assert store.website == 'https://teststore.com'
        assert store.picture.name.startswith('media/store_pictures/test_picture')
        assert store.owner.first_name == 'konul'

    def test_store_string_representation(self, store):
        assert str(store) == 'Test Store'
    

    def test_store_address_optional(self, store):
        '''Test creating a store without address'''
        store.address = None  # Set the address field to None
        store.save()
        assert store.address is None
        

    def test_store_without_name(self, user):
        store = StoreModel(
        owner=user,
        description='This store has no name.',
        address='123 Test Street',
        website='https://teststore.com'
    )
        with pytest.raises(ValidationError):
            store.full_clean()  # Validate the store, expecting a ValidationError

    
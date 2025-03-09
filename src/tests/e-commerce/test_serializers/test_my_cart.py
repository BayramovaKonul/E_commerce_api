import pytest
from rest_framework.exceptions import ValidationError
from rest_framework.test import APIClient
from e_commerce.models import CartModel
from products.models import ProductModel
from e_commerce.serializers import MyCartSerializer
from tests.confest import user, product, cart_item, category, store

@pytest.mark.django_db
class TestMyCartSerializer:
    def test_item_total_calculation(self, cart_item):
        ''' Test that item_total is correctly calculated'''
        serializer = MyCartSerializer(cart_item)
        assert serializer.data['item_total'] == 20.00  # 2 * 100 (quantity * price)
    

    def test_product_serialization(self, cart_item):
        ''' Test that product is correctly serialized with only the expected fields ('name' and 'price')'''
        serializer = MyCartSerializer(cart_item)
        assert 'product' in serializer.data
        assert 'name' in serializer.data['product']
        assert 'price' in serializer.data['product']
        assert not 'description' in serializer.data


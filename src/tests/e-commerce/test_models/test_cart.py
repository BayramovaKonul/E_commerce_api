import pytest
from e_commerce.models import CartModel
from tests.confest import user, product, category, store
from django.db import IntegrityError, transaction

@pytest.mark.django_db
class TestCartModel:

    def test_cart_creation(self, user, product):
        """Test that a cart entry can be created"""
        cart_item = CartModel.objects.create(user=user, product=product)

        assert cart_item.user == user
        assert cart_item.product == product
        assert CartModel.objects.count() == 1


    def test_cart_str_representation(self, user, product):
        """Test the string representation of CartModel"""
        cart_item = CartModel.objects.create(user=user, product=product)

        expected_str = f"{user.email} -> {cart_item.product.name}"
        assert str(cart_item) == expected_str

    
    def test_unique_user_product_cart(self, user, product):
        """Test that a user cannot add the same product to the cart twice"""
        
        CartModel.objects.create(user=user, product=product)

        with pytest.raises(Exception) as excinfo:
            CartModel.objects.create(user=user, product=product)
        
        assert 'unique constraint' in str(excinfo.value).lower()

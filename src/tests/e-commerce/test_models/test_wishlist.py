import pytest
from e_commerce.models import WishlistModel
from tests.confest import user, product, category, store
from django.db import IntegrityError, transaction

@pytest.mark.django_db
class TestWishlistModel:

    def test_wishlist_creation(self, user, product):
        """Test that a wishlist entry can be created"""
        wishlist = WishlistModel.objects.create(user=user, product=product)

        assert wishlist.user == user
        assert wishlist.product == product
        assert WishlistModel.objects.count() == 1


    def test_wishlist_str_representation(self, user, product):
        """Test the string representation of WishlistModel"""
        wishlist = WishlistModel.objects.create(user=user, product=product)

        expected_str = f"{user.email} -> {wishlist.created_at}"
        assert str(wishlist) == expected_str

    
    def test_unique_user_product_wishlist(self, user, product):
        """Test that a user cannot add the same product to the wishlist twice"""
        
        WishlistModel.objects.create(user=user, product=product)

        with pytest.raises(Exception) as excinfo:
            WishlistModel.objects.create(user=user, product=product)
        
        assert 'unique constraint' in str(excinfo.value).lower()

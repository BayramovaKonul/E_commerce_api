import pytest
from rest_framework.exceptions import ValidationError
from e_commerce.models import WishlistModel
from e_commerce.serializers import AddWishlistSerializer
from tests.confest import user, product, store, category
from rest_framework.test import APIRequestFactory
from django.urls import reverse

@pytest.mark.django_db
class TestAddWishlistSerializer:

    def test_valid_add_wishlist(self, user, product):
        """Test that a product can be added to the wishlist"""
    
        factory = APIRequestFactory()
        url = reverse('list_add_wishlist')    
        request = factory.post(url)  
        request.user = user
        product_data={
            'product':product.id
        }
        serializer = AddWishlistSerializer(data=product_data, context={'request': request})

        assert serializer.is_valid()
        serializer.save()

        assert WishlistModel.objects.filter(user=user, product=product).exists()


    def test_duplicate_product_in_wishlist(self, user, product):
        """Test that a product cannot be added twice to the wishlist"""

        WishlistModel.objects.create(user=user, product=product)

        factory = APIRequestFactory()
        url = reverse('list_add_wishlist')  
        request = factory.post(url)  
        request.user = user
        product_data={
            'product':product.id
        }
        serializer = AddWishlistSerializer(data=product_data, context={'request': request})

        with pytest.raises(ValidationError) as exc_info:
            serializer.is_valid(raise_exception=True)
        
        # Assert that the error message matches the custom message
        assert "This product is already in your wishlist." in str(exc_info.value)

        assert WishlistModel.objects.filter(user=user, product=product).count() == 1

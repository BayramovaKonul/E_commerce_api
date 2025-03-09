import pytest
from rest_framework.exceptions import ValidationError
from e_commerce.models import CartModel
from e_commerce.serializers import AddToCartSerializer
from tests.confest import user, product, store, category
from rest_framework.test import APIRequestFactory
from django.urls import reverse

@pytest.mark.django_db
class TestAddToCartSerializer:

    def test_valid_add_to_cart(self, user, product):
        """Test that a product can be added to the cart"""
    
        factory = APIRequestFactory()
        url = reverse('add_to_cart', kwargs={'product_id': product.id})    
        request = factory.post(url)  
        request.user = user
        serializer = AddToCartSerializer(data={'product': product.id}, context={'request': request})

        assert serializer.is_valid()
        serializer.save()

        assert CartModel.objects.filter(user=user, product=product).exists()


    def test_duplicate_product_in_cart(self, user, product):
        """Test that a product cannot be added twice to the cart"""

        CartModel.objects.create(user=user, product=product)

        factory = APIRequestFactory()
        url = reverse('add_to_cart', kwargs={'product_id': product.id})  
        request = factory.post(url)  
        request.user = user

        serializer = AddToCartSerializer(data={'product': product.id}, context={'request': request})

        with pytest.raises(ValidationError) as exc_info:
            serializer.is_valid(raise_exception=True)
        
        # Assert that the error message matches the custom message
        assert "This product is already in your cart." in str(exc_info.value)

        assert CartModel.objects.filter(user=user, product=product).count() == 1

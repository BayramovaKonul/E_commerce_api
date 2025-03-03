import pytest
from rest_framework import status
from django.urls import reverse
from e_commerce.models import CartModel
from tests.confest import authenticated_client, user, product, store, category, anonymous_client, another_authenticated_client, another_user

@pytest.mark.django_db
class TestAddToCartView:

    def test_add_product_to_cart(self, authenticated_client, user, product):
        """Test that a product can be added to the cart."""
        
        url = reverse('add_to_cart', kwargs={'product_id': product.id})
        response = authenticated_client.post(url)

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['message'] == "You added a product to your cart"

        assert CartModel.objects.filter(user=user, product=product).exists()


    def test_add_duplicate_product_to_cart(self, authenticated_client, user, product):
        """Test that a duplicate product cannot be added to the cart."""

        CartModel.objects.create(user=user, product=product)

        url = reverse('add_to_cart', kwargs={'product_id': product.id})

        response = authenticated_client.post(url)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert str(response.data['product'][0]) == "This product is already in your cart."

        assert CartModel.objects.filter(user=user, product=product).count() == 1


    def test_add_product_to_cart_invalid_product(self, authenticated_client, user):
        """Test that adding a non-existent product returns a 404 error."""

        url = reverse('add_to_cart', kwargs={'product_id': 9999})  

        response = authenticated_client.post(url)

        assert response.status_code == status.HTTP_400_BAD_REQUEST


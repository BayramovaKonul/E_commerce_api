import pytest
from decimal import Decimal
from django.core.exceptions import ValidationError
from products.models import ProductModel
from ...confest import store, category, user

@pytest.mark.django_db
class TestProductModel:

    def test_create_product_with_valid_data(self, user, store, category):
        """Test that a product can be created with valid data"""
        product = ProductModel.objects.create(
            name="Test Product",
            description="A sample product",
            price=Decimal('10.00'),
            stock=100,
            store=store
        )
        product.categories.add(category)

        assert product.name == "Test Product"
        assert product.description == "A sample product"
        assert product.price == Decimal('10.00')
        assert product.stock == 100
        assert product.store == store
        assert product.categories.count() == 1
        assert product.categories.first() == category


    def test_product_invalid_price(self, store):
        """Test that a product with an invalid price raises a validation error"""
        with pytest.raises(ValidationError):
            product = ProductModel(
                name="Invalid Product",
                description="Product with invalid price",
                price=Decimal('0.00'),
                stock=50,
                store=store
            )

            product.full_clean()  # This will trigger the validation

    
    def test_product_invalid_stock(self, store):
        """Test that a product with an invalid stock raises a validation error"""
        with pytest.raises(ValidationError):
            product = ProductModel(
                name="Invalid Product",
                description="Product with invalid price",
                price=Decimal('1.99'),
                stock=-5,
                store=store
            )

            product.full_clean()  


    def test_invalid_product_with_missing_fields(self, store):
        """Test that a product cannot be created without required fields"""
        with pytest.raises(ValidationError):
            product = ProductModel.objects.create(
                name="",  
                description="Test description",
                price=Decimal('10.00'),
                stock=50,
                store=store
            )

            product.full_clean()


         
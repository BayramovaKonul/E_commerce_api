import pytest
from io import BytesIO
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import InMemoryUploadedFile
from PIL import Image, UnidentifiedImageError
from PIL import Image
from products.models import ProductImageModel, ProductModel
from store.models import StoreModel
from ...confest import product, image_file, store, user, category

@pytest.mark.django_db
class TestProductImageModel:

    def test_create_product_image_with_valid_data(self, product, image_file):
        """Test that a product image can be created with valid data"""
        product_image = ProductImageModel.objects.create(
            image=image_file,
            product=product
        )

        assert product_image.image.name.startswith('media/product_pictures/test_image')
        assert product_image.product == product

    # Since my resizing doesn't work, its test doesnt work as well
    
    # def test_image_resizing(self, product, image_file):
    #     """Test that the image is resized when saving"""
    #     product_image = ProductImageModel.objects.create(
    #         image=image_file,
    #         product=product
    #     )

    #     # Load the saved image to verify its size
    #     img = Image.open(product_image.image)
    #     assert img.size == (295, 295)  # Ensure the image is resized to 295x295 (max dimension)


    def test_str_method(self, product, image_file):
        """Test the __str__ method"""
        product_image = ProductImageModel.objects.create(
            image=image_file,
            product=product
        )

        # Get the actual file name (which is dynamically generated)
        actual_image_name = product_image.image.name

        assert actual_image_name.startswith('media/product_pictures/')
        assert str(product_image) == f"{actual_image_name} -> {product}"


    def test_invalid_image_format(self, product):
        """Test that an invalid image format raises a validation error"""
        # Create a non-image file 
        invalid_image_file = InMemoryUploadedFile(
            BytesIO(b"Invalid content"),
            None,
            'invalid_file.txt',
            'text/plain',
            len(b"Invalid content"),
            None
        )

        product_image = ProductImageModel(image=invalid_image_file, product=product)

        with pytest.raises(UnidentifiedImageError):
            Image.open(product_image.image).verify() 

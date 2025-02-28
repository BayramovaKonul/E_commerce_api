from django.db import models
from django.utils.translation import gettext as _
from .product import ProductModel
from store.models import CreationDateAbstractModel
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile


class ProductImageModel(CreationDateAbstractModel):
    image = models.ImageField(verbose_name=_("image"), upload_to="media/product_pictures")
    product = models.ForeignKey(ProductModel, related_name="images", on_delete=models.CASCADE, verbose_name=_("product"))

    
    class Meta:
        db_table = _('product_images')
        verbose_name = _('Product Image')
        verbose_name_plural = _('Product Images')


    def __str__(self):
        return f"{self.image} -> {self.product}"
    
    def save(self, *args, **kwargs):
        # Open the image using Pillow
        if self.image:
            img = Image.open(self.image)
            img = img.convert('RGB')  # Ensure it's in RGB mode

            # Resize the image while maintaining the aspect ratio
            img.thumbnail((295, 295))

            # Save the resized image to a BytesIO object
            img_io = BytesIO()
            img.save(img_io, format='JPEG')  # Save it as JPEG
            img_io.seek(0)

            # Replace the image file with the resized image
            self.image = InMemoryUploadedFile(
                img_io, None, self.image.name, 'image/jpeg', img_io.tell(), None
            )

        # Call the superclass save method to save the object
        super().save(*args, **kwargs)
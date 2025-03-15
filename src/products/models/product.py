from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _
from store.models import StoreModel, CreationDateAbstractModel
from .category import CategoryModel
from django.core.validators import MinValueValidator

User=get_user_model()

class ProductModel (CreationDateAbstractModel):
    name = models.CharField(verbose_name=_("name"), max_length=255)
    description = models.TextField(verbose_name=_("description"), max_length=500)
    price = models.DecimalField(verbose_name=_("price"), decimal_places=2, max_digits=10, 
                                validators=[MinValueValidator(0.01)])
    stock = models.PositiveIntegerField(verbose_name=_("stock"))
    store = models.ForeignKey(StoreModel, on_delete=models.SET_NULL, null=True,
                               related_name="products", verbose_name=_("products"))
    categories = models.ManyToManyField(CategoryModel,
                                        related_name="products", verbose_name=_("products"))

    class Meta:
        db_table = _('product')
        verbose_name = _('Product')
        verbose_name_plural = _('Products')

    def __str__(self):
        return f"{self.name} -> {self.stock}"
    
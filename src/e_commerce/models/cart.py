from django.db import models
from django.utils.translation import gettext as _
from products.models.product import ProductModel
from django.core.validators import MinValueValidator
from django.contrib.auth import get_user_model
from store.models.creation_date_abstract import CreationDateAbstractModel

User=get_user_model()
class CartModel (CreationDateAbstractModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, 
                              related_name="cart", verbose_name=_("user"))
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE, 
                              related_name="cart", verbose_name=_("product"))
    quantity = models.PositiveIntegerField(verbose_name=_("quantity"), default = 1)
    
    
    class Meta:
        db_table = _('cart')
        verbose_name = _('Cart')
        verbose_name_plural = _('Carts')
        unique_together = ('user', 'product')


    def __str__(self):
        return f"{self.user.email} -> {self.product.name}"
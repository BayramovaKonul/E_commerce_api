from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _
from products.models.product import ProductModel
from store.models.creation_date_abstract import CreationDateAbstractModel

User = get_user_model()

class WishlistModel(CreationDateAbstractModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, 
                             related_name="wishlists", verbose_name=_("user"))
    product = models.ForeignKey(ProductModel, on_delete= models.CASCADE,
                                    related_name="wishlists", verbose_name=_("product"))
    
    class Meta:
        db_table = _('wishlist')
        verbose_name = _('Wishlist')
        verbose_name_plural = _('Wishlists')
        unique_together = ('user', 'product')

    def __str__(self):
        return f"{self.user.email} -> {self.created_at}"
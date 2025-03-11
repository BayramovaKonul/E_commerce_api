from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _
from .product import ProductModel
from store.models.creation_date_abstract import CreationDateAbstractModel
from django.core.validators import MinValueValidator, MaxValueValidator

User = get_user_model()

class CommentModel(CreationDateAbstractModel):
    comment = models.CharField(verbose_name=_("comment"))
    rating = models.IntegerField(verbose_name=_("rating"), 
                                 validators=[MinValueValidator(1), MaxValueValidator(5)], null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, 
                             related_name="comments")
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE, 
                             related_name="comments")

    
    class Meta:
        db_table = _('comment')
        verbose_name = _('Comment')
        verbose_name_plural = _('Comments')

    def __str__(self):
        return f"{self.comment} -> {self.rating}"
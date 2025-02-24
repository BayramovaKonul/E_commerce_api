from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _

class CategoryModel(models.Model):
    name = models.CharField(verbose_name=_("name"), max_length=150)
    created_at = models.DateTimeField(verbose_name=_("created_at"), auto_now_add=True)

    
    class Meta:
        db_table = _('category')
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')

    def __str__(self):
        return f"{self.name}"
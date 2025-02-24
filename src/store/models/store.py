from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _
from .creation_date_abstract import CreationDateAbstractModel

User=get_user_model()


class StoreModel (CreationDateAbstractModel):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, 
                              related_name="stores", verbose_name=_("owner"))
    name = models.CharField(verbose_name=_("name"), max_length=255, blank=False)
    description = models.TextField(verbose_name=_("description"), blank=False)
    address = models.CharField(verbose_name=_("address"), null=True, max_length=255)
    website = models.CharField(verbose_name=_("website"), null=True, max_length=100)
    picture = models.ImageField(verbose_name=_("picture"), upload_to="media/store_pictures")

    class Meta:
        db_table = _('stores')
        verbose_name = _('Store')
        verbose_name_plural = _('Stores')

    def __str__(self):
        return f"{self.name}"


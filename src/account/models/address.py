from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _
from store.models.creation_date_abstract import CreationDateAbstractModel

User=get_user_model()


class AddressModel (CreationDateAbstractModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, 
                              related_name="address", verbose_name=_("user"))
    address = models.CharField(verbose_name=_("addresses"), max_length=200)
    country = models.CharField(verbose_name=_("country"), max_length=100)
    city = models.CharField(verbose_name=_("city"), max_length=100)
    zip_code = models.CharField(verbose_name=_("zip_code"), max_length=20)
    is_default = models.BooleanField(default=False)
    

    class Meta:
        db_table = _('address')
        verbose_name = _('Address')
        verbose_name_plural = _('Addresses')

    def __str__(self):
        return f"{self.address} -> {self.city}"


from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _
from account.models.address import AddressModel

User=get_user_model()


class OrderModel (models.Model):

    class OrderStatus(models.TextChoices):
        PENDING = 'pending', 'Pending'
        COMPLETED = 'completed', 'Completed'


    user = models.ForeignKey(User, on_delete=models.CASCADE, 
                              related_name="orders", verbose_name=_("user"))
    shipping_address = models.ForeignKey(AddressModel,on_delete=models.SET_NULL, 
                                         verbose_name=_("shipping_address"), related_name="orders", null=True)
    status = models.CharField(verbose_name=_("status"), choices=OrderStatus.choices, default=OrderStatus.PENDING)
    created_at = models.DateTimeField(verbose_name=_("created_at"), auto_now_add=True)
    
    
    class Meta:
        db_table = _('order')
        verbose_name = _('Order')
        verbose_name_plural = _('Orders')

    def __str__(self):
        return f"{self.shipping_address.country} -> {self.status}"


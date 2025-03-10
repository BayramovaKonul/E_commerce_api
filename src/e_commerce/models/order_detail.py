from django.db import models
from django.utils.translation import gettext as _
from e_commerce.models.order import OrderModel
from products.models.product import ProductModel
from django.core.validators import MinValueValidator

class OrderDetailsModel (models.Model):

    class ProductStatus(models.TextChoices):
        PENDING = 'pending', 'Pending'
        PAYMENT_RECEIVED = 'payment_received', 'Payment Received'
        PROCESSING = 'processing', 'Processing'
        PACKAGED = 'packaged', 'Packaged'
        SHIPPED = 'shipped', 'Shipped'
        OUT_FOR_DELIVERY = 'out_for_delivery', 'Out for Delivery'
        LOCAL_DELIVERY_CENTER = 'in_the_local_delivery_center', 'In the Local Delivery Center'
        GIVEN_TO_COURIER = 'given_to_courier', 'Given to Courier'
        DELIVERED = 'delivered', 'Delivered'

    order = models.ForeignKey(OrderModel, on_delete=models.CASCADE, 
                              related_name="details", verbose_name=_("order"))
    product = models.ForeignKey(ProductModel, on_delete=models.DO_NOTHING, 
                              related_name="details", verbose_name=_("product"))
    quantity = models.IntegerField(verbose_name=_("quantity"), validators=[MinValueValidator(1)])
    cost = models.DecimalField(verbose_name=_("cost"), max_digits=10, decimal_places=2)  # one-item-cost
    status = models.CharField(verbose_name=_("status"), choices=ProductStatus.choices, default=ProductStatus.PENDING)
    
    
    class Meta:
        db_table = _('order_detail')
        verbose_name = _('Order_detail')
        verbose_name_plural = _('Order details')

    def __str__(self):
        return f"{self.product.name} -> {self.status} -> {self.cost}"


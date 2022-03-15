import uuid
from django.db import models

from common.utils import get_dollar_price

from ..product.models import Product
from django.db.models import F


class Order(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date_time = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def get_total(self):

        total = sum(self.orderdetail_set.all().annotate(subtotal=F('cuantity') * F('product__price')
                                                        ).values_list('subtotal', flat=True))
        return round(total, 4)

    def get_total_usd(self):

        dollar_price = get_dollar_price()

        return round(self.get_total() / dollar_price, 4)


class OrderDetail(models.Model):
    class Meta:
        unique_together = (('order'), ('product'))

    cuantity = models.PositiveIntegerField()

    order = models.ForeignKey(Order, null=True, on_delete=models.SET_NULL)
    product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL)

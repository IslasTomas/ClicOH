import uuid
from django.db import models, transaction

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

    def restore_stock_products(self):
        try:
            with transaction.atomic():
                for detail in self.orderdetail_set.all():

                    detail.restore_stock()
                return True
        except Exception:
            return False


class OrderDetail(models.Model):
    class Meta:
        unique_together = (('order'), ('product'))

    cuantity = models.PositiveIntegerField()

    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL)

    def restore_stock(self):
        try:
            with transaction.atomic():
                self.product.stock += self.cuantity
                self.product.save()
                return True
        except Exception:
            return False

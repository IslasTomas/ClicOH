import uuid
from django.db import models

from ..product.models import Product


class Order(models.Model):
    pid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    


    def get_total(self):
        """return the total of the order"""
        pass

    def get_total_usd(self):
        """return the total of the order in dollars"""
        pass


class OrderDetail(models.Model):

    cuantity = models.PositiveIntegerField()

    order = models.ForeignKey(Order, null=True, on_delete=models.SET_NULL)
    product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL)
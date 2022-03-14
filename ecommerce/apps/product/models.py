import uuid
from django.db import models

class Product(models.Model):

    pid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=150, unique=True)
    price = models.FloatField()
    stock = models.PositiveIntegerField(default=0)
    
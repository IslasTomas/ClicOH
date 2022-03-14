from rest_framework import serializers
from .models import Product


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ('id',
                  'name',
                  'price',
                  'stock',
                  )
        extra_kwargs = {
            'id': {'read_only': True}
        }


class ProductStockserializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            'id',
            'stock',
            'name',
            'price',

        )

    # read_only_fields = ('id', 'name', 'price')

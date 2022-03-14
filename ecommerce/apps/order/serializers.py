from rest_framework import serializers
from .models import Order, OrderDetail


class OrderDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderDetail
        fields = ('cuantity', 'order', 'price')


class OrderSerializer(serializers.ModelSerializer):
    total_price = serializers.SerializerMethodField()
    total_price_usd = serializers.SerializerMethodField()
    order_details = OrderDetailSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ('id',
                  'date_time',
                  )
        extra_kwargs = {
            'id': {'read_only': True},
            'total_price': {'read_only': True},
            'total_price_usd': {'read_only': True}

        }

    def get_total_price(self, value):
        pass

    def get_total_price_usd(self, value):
        pass

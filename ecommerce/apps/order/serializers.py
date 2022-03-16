from django.db.models import Q

from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueTogetherValidator

from apps.product.serializers import ProductSerializer
from .models import Order, OrderDetail


class OrderDetailSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = OrderDetail
        fields = ('cuantity', 'product',)


class OrderSerializer(serializers.ModelSerializer):
    total_price = serializers.SerializerMethodField()
    total_price_usd = serializers.SerializerMethodField()
    order_details = OrderDetailSerializer(
        many=True, source='orderdetail_set')

    def get_total_price(self, instance):

        return instance.get_total()

    def get_total_price_usd(self, instance):
        return instance.get_total_usd()

    class Meta:
        model = Order
        fields = ('id',
                  'date_time',
                  'order_details',
                  'total_price',
                  'total_price_usd',
                  )
        read_only_fields = ('id', 'total_price', 'total_price_usd')


class OrderDetailCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderDetail
        fields = ('cuantity', 'product',)

    def validate(self, data):

        if data['cuantity'] <= 0:
            raise ValidationError(
                detail=('cuantity must be greater than 0'))

        remaining_stock = data['product'].stock - data['cuantity']
        if remaining_stock < 0:
            raise ValidationError(
                detail=(f'out of stock, stock:{data["product"].stock}'))

        self.context['remaining_stock'] = remaining_stock
        return data

    def create(self, validated_data):
        instance = OrderDetail.objects.create(
            order=self.context['order'], **validated_data)
        validated_data['product'].stock = self.context['remaining_stock']
        validated_data['product'].save()
        return instance


class OrderCreateSerializer(serializers.ModelSerializer):
    orderdetail_set = OrderDetailCreateSerializer(
        many=True, source='orderdetail_set')

    class Meta:
        model = Order
        fields = (

            'order_details',
        )

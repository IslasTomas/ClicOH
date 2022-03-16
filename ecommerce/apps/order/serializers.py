from django.db.models import Q

from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueTogetherValidator

from apps.product.serializers import ProductSerializer
from .validates import validate_data_order_detail
from .models import Order, OrderDetail


class OrderDetailSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = OrderDetail
        fields = ('id', 'cuantity', 'product',)

        read_only_fields = ('id',)


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
        if OrderDetail.objects.filter(product=data.product, orders=self.context['order']).exists():
            raise ValidationError(
                detail=('The fields order, product must make a unique set."'))
        return validate_data_order_detail(self, data)

    def create(self, validated_data):

        instance = OrderDetail.objects.create(
            order=self.context['order'], **validated_data)

        validated_data['product'].stock = self.context['remaining_stock']
        validated_data['product'].save()
        return instance


class OrderCreateSerializer(serializers.ModelSerializer):
    order_details = OrderDetailCreateSerializer(
        many=True, source='orderdetail_set')

    class Meta:
        model = Order
        fields = (
            'order_details',
        )


class OrderDetailCreateviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderDetail
        fields = ('order', 'cuantity', 'product',)

        validators = [
            UniqueTogetherValidator(
                queryset=OrderDetail.objects.all(),
                fields=['order', 'product']
            )
        ]

    def validate(self, data):

        if not data.get('product'):
            data['partial'] = True
            data['product'] = self.instance.product
        return validate_data_order_detail(self, data)

    def create(self, data):
        instance = super(OrderDetailCreateviewSerializer,
                         self).create(data)
        instance.product.save()
        return instance

    def update(self, instance, data):
        instance = super(OrderDetailCreateviewSerializer,
                         self).update(instance, data)
        instance.product.save()
        return instance

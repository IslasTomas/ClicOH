from multiprocessing import context
from rest_framework import viewsets, status
from rest_framework.response import Response
from django.db import transaction
from .serializers import OrderCreateSerializer, OrderDetailCreateSerializer, OrderDetailCreateviewSerializer, OrderDetailSerializer, OrderSerializer


from .models import Order, OrderDetail
# Create your views here.


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializers = {
        'default': OrderSerializer,
        'create': OrderCreateSerializer,

    }

    def get_serializer_class(self):
        """
        returns serializer depending on the field  self.action
        """
        return self.serializers.get(
            self.action, self.serializers["default"])

    @transaction.atomic
    def create(self, request, *args, **kwargs):

        instance = Order.objects.create()

        serializer = OrderDetailCreateSerializer(
            data=request.data['order_details'], many=True, context={'order': instance})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        serializer_response = OrderSerializer(instance)
        return Response(serializer_response.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        return Response({}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def destroy(self, request, *args, **kwargs):

        instance = self.get_object()
        restored = instance.restore_stock_products()

        if restored:
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(data={'response': 'Internal error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class OrderDetailViewSet(viewsets.ModelViewSet):
    queryset = OrderDetail.objects.all()

    serializers = {
        'default': OrderDetailSerializer,
        'create': OrderDetailCreateviewSerializer,
        'update': OrderDetailCreateviewSerializer,
        'partial_update': OrderDetailCreateviewSerializer

    }

    def get_serializer_class(self):
        """
        returns serializer depending on the field  self.action
        """
        return self.serializers.get(
            self.action, self.serializers["default"])

    def destroy(self, request, *args, **kwargs):

        instance = self.get_object()
        restored = instance.restore_stock()
        if restored:
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(data={'response': 'Internal error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

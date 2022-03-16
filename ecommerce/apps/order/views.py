from multiprocessing import context
from rest_framework import viewsets, status
from rest_framework.response import Response

from .serializers import OrderCreateSerializer, OrderDetailCreateSerializer, OrderSerializer

from .models import Order
# Create your views here.


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializers = {
        'default': OrderSerializer,
        'create': OrderCreateSerializer,
        'update_stock': OrderSerializer,
    }

    def get_serializer_class(self):
        """
        returns serializer depending on the field  self.action
        """
        return self.serializers.get(
            self.action, self.serializers["default"])

    def create(self, request, *args, **kwargs):
        instance = Order.objects.create()

        serializer = OrderDetailCreateSerializer(
            data=request.data['order_details'], many=True, context={'order': instance})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        serializer_response = OrderSerializer(instance)
        return Response(serializer_response.data, status=status.HTTP_201_CREATED)

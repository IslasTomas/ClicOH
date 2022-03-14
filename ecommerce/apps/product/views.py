# rest
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response


# models
from .models import Product

# serializers
from .serializers import ProductSerializer, ProductStockserializer

# filters
from .filters import ProductFilter


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializers = {
        'default': ProductSerializer,
        'update_stock': ProductStockserializer,
    }
    filterset_class = ProductFilter
    search_fields = ['name', ]
    ordering_fields = ['name', 'price', 'stock']
    ordering = ['name', ]

    def get_serializer_class(self):
        """
        returns serializer depending on the field  self.action
        """
        return self.serializers.get(
            self.action, self.serializers["default"])

    @action(methods=['patch'], detail=True, url_name='update-stock', url_path='update_stock')
    def update_stock(self, request, *args, **kwargs):
        product = self.get_object()
        serializer = ProductSerializer(
            product, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)

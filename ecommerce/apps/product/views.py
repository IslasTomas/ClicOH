# rest
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser

# models
from .models import Product

# serializers
from .serializers import ProductSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializers = {
        'default': ProductSerializer,
        'create': ProductSerializer,
        'update': ProductSerializer,
        'partial_update': ProductSerializer
    }

    # ordering_fields = ('')
    # ordering = ('')

    def get_serializer_class(self):
        """
        Devuelve un serializador en función del verbo HTTP.
        Si no está definido, devuelve el serializador
        por defecto.
        """

        return self.serializers.get(
            self.action, self.serializers["default"])

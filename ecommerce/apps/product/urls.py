from rest_framework.routers import DefaultRouter

from .views import ProductViewSet


app_name="order"

router = DefaultRouter()

router.register(r'product',ProductViewSet,basename='product')

urlpatterns = []

urlpatterns += router.urls
from rest_framework.routers import DefaultRouter

from .views import OrderDetailViewSet, OrderViewSet


app_name = "order"

router = DefaultRouter()

router.register(r'orders', OrderViewSet, basename='order')
router.register(r'order/details', OrderDetailViewSet, basename='order-detail')


urlpatterns = []

urlpatterns += router.urls

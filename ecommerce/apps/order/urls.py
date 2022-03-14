from rest_framework.routers import DefaultRouter

from .views import OrderViewSet


app_name="order"

router = DefaultRouter()

router.register(r'order',OrderViewSet,basename='order')

urlpatterns = []

urlpatterns += router.urls
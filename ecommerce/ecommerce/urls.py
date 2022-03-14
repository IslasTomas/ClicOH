from django.conf import settings
from django.conf.urls import include
from django.contrib import admin
from django.urls import path

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [

    path('admin/', admin.site.urls),

    path(f'api/{settings.VERSION}/token/',TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path(f'api/{settings.VERSION}/token/refresh/',
         TokenRefreshView.as_view(), name='token_refresh'),

    path(f'api/{settings.VERSION}/',
       include('apps.order.urls',namespace='order')),
    path(f'api/{settings.VERSION}/',
       include('apps.product.urls',namespace='product')),    
 ]
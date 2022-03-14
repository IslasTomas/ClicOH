from django.conf import settings


from django.contrib import admin
from django.urls import path, re_path, include

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework import permissions

from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView


urlpatterns = [

    path('schema', SpectacularAPIView.as_view(), name='schema'),

    path('swagger/',
         SpectacularSwaggerView.as_view(url_name='schema'), name='swagger'),

    path('admin/', admin.site.urls),

    path(f'api/{settings.VERSION}/token/',
         TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path(f'api/{settings.VERSION}/token/refresh/',
         TokenRefreshView.as_view(), name='token_refresh'),

    path(f'api/{settings.VERSION}/',
         include('apps.order.urls', namespace='order')),
    path(f'api/{settings.VERSION}/',
         include('apps.product.urls', namespace='product'))
]

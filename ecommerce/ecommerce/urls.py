from django.conf import settings


from django.contrib import admin
from django.urls import path, re_path, include

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework import permissions

from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
    openapi.Info(
        title="TSA Api",
        default_version='v1',
        description="API documentation",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="testing@api.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    re_path(r'^swagger/$', schema_view.with_ui('swagger',
        cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^docs/$', schema_view.with_ui('redoc',
        cache_timeout=0), name='schema-redoc'),
    path('admin/', admin.site.urls),

    path(f'api/{settings.VERSION}/token/',TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path(f'api/{settings.VERSION}/token/refresh/',
         TokenRefreshView.as_view(), name='token_refresh'),

    path(f'api/{settings.VERSION}/',
       include('apps.order.urls',namespace='order')),
    path(f'api/{settings.VERSION}/',
       include('apps.product.urls',namespace='product')),    
 ]
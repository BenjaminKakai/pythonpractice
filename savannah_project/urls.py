# savannah_project/urls.py
from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
# Add this import for health check
from savannah_app.health_views import health_check  # Add this line

# Schema view configuration for API documentation
schema_view = get_schema_view(
    openapi.Info(
        title="Savannah API",
        default_version='v1',
        description="API documentation for Savannah E-commerce",
        terms_of_service="https://www.yourapp.com/terms/",
        contact=openapi.Contact(email="contact@yourapp.com"),
        license=openapi.License(name="Your License"),
    ),
    public=True,
)

urlpatterns = [
    # Health check
    path('health/', health_check, name='health_check'),
    
    # Admin interface
    path('admin/', admin.site.urls),
    
    # API Documentation
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    
    # Authentication endpoints
    path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/auth/', include('rest_framework.urls')),
    
    # API endpoints
    path('api/v1/', include('savannah_app.urls')),
    path('', include('savannah_app.urls')),  # Default route
]
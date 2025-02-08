# savannah_app/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CategoryViewSet,
    ProductViewSet,
    OrderViewSet,
    CustomerViewSet
)

router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'products', ProductViewSet)
router.register(r'orders', OrderViewSet, basename='order')  # Added basename
router.register(r'customers', CustomerViewSet, basename='customer')  # Added basename for consistency

urlpatterns = [
    path('', include(router.urls)),
]
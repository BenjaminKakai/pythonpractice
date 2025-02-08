# views.py
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from django.db.models import Avg
from .models import Category, Product, Customer, Order
from .serializers import CategorySerializer, ProductSerializer, CustomerSerializer, OrderSerializer
from .permissions import IsAdminUser, IsCustomer
from .utils import send_order_notification

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminUser()]
        return [IsAuthenticated()]
    
    @action(detail=False, methods=['post'])
    def bulk_upload(self, request):
        """Upload multiple products at once."""
        serializer = ProductSerializer(data=request.data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def by_category(self, request):
        """Get products filtered by category."""
        category_id = request.query_params.get('category_id')
        if category_id:
            products = self.queryset.filter(category_id=category_id)
            page = self.paginate_queryset(products)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            serializer = self.get_serializer(products, many=True)
            return Response(serializer.data)
        return Response(
            {"error": "Category ID is required"}, 
            status=status.HTTP_400_BAD_REQUEST
        )

class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated, IsCustomer]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Order.objects.all()
        return Order.objects.filter(customer__user=self.request.user)

    def perform_create(self, serializer):
        """Create order and send notification."""
        # Ensure the customer is set to the current user's customer profile
        customer = Customer.objects.get(user=self.request.user)
        order = serializer.save(customer=customer)
        send_order_notification(order)

    @action(detail=True, methods=['post'])
    def update_status(self, request, pk=None):
        """Update order status (admin only)."""
        if not request.user.is_staff:
            return Response(
                {"error": "Admin access required"}, 
                status=status.HTTP_403_FORBIDDEN
            )
            
        order = self.get_object()
        new_status = request.data.get('status')
        if new_status not in dict(Order.STATUS_CHOICES):
            return Response(
                {"error": "Invalid status"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
            
        order.status = new_status
        order.save()
        send_order_notification(order)
        return Response({
            "status": "updated",
            "new_status": new_status,
            "order_number": order.order_number
        })

    @action(detail=False, methods=['get'])
    def history(self, request):
        """Get order history for current user."""
        orders = self.get_queryset().order_by('-created_at')
        # Add filtering options
        status_filter = request.query_params.get('status')
        if status_filter:
            orders = orders.filter(status=status_filter)
            
        page = self.paginate_queryset(orders)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(orders, many=True)
        return Response(serializer.data)
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from django.db.models import Avg
from .models import Category, Product, Customer, Order
from .serializers import CategorySerializer, ProductSerializer, CustomerSerializer, OrderSerializer
from .permissions import IsAdminUser, IsCustomer
from .utils import send_order_notification, send_order_confirmation

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['get'])
    def average_price(self, request, pk=None):
        """Get average product price for a category."""
        category = self.get_object()
        average = category.products.aggregate(avg_price=Avg('price'))['avg_price']
        
        # Include child categories in calculation
        for child in category.get_descendants():
            child_avg = child.products.aggregate(avg_price=Avg('price'))['avg_price']
            if child_avg is not None:
                if average is None:
                    average = child_avg
                else:
                    average = (average + child_avg) / 2

        return Response({
            'category': category.name,
            'average_price': average if average is not None else 0
        })

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

class CustomerViewSet(viewsets.ModelViewSet):
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        if self.request.user.is_staff:
            return Customer.objects.all()
        return Customer.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated, IsCustomer]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Order.objects.all()
        return Order.objects.filter(customer__user=self.request.user)

    def perform_create(self, serializer):
        """Create order and send notification."""
        try:
            customer = Customer.objects.get(user=self.request.user)
            order = serializer.save(customer=customer)
            # Send initial order confirmation
            send_order_confirmation(order)
        except Customer.DoesNotExist:
            raise serializer.ValidationError("Customer profile not found")

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
            
        old_status = order.status
        order.status = new_status
        order.save()
        
        # Send status update notification
        send_order_notification(order)
        
        return Response({
            "status": "updated",
            "old_status": old_status,
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
# savannah_app/management/commands/create_sample_data.py
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from savannah_app.models import Category, Product, Customer, Order, OrderItem
from decimal import Decimal
import random

class Command(BaseCommand):
    help = 'Creates sample data for testing'

    def handle(self, *args, **kwargs):
        # Create categories
        grocery = Category.objects.create(name='Grocery', slug='grocery')
        bakery = Category.objects.create(name='Bakery', slug='bakery', parent=grocery)
        produce = Category.objects.create(name='Produce', slug='produce', parent=grocery)
        
        # Create some products
        products = [
            Product.objects.create(
                name='Whole Wheat Bread',
                slug='whole-wheat-bread',
                description='Fresh whole wheat bread',
                price=Decimal('3.99'),
                category=bakery,
                stock=100
            ),
            Product.objects.create(
                name='Fresh Apples',
                slug='fresh-apples',
                description='Crisp fresh apples',
                price=Decimal('1.99'),
                category=produce,
                stock=200
            )
        ]

        # Create a test user and customer
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        customer = Customer.objects.create(
            user=user,
            phone='1234567890',
            address='123 Test St',
            city='Test City',
            country='Test Country',
            postal_code='12345'
        )

        self.stdout.write(self.style.SUCCESS('Successfully created sample data'))
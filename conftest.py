import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from savannah_app.models import Category, Product, Customer, Order, OrderItem

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def user():
    return User.objects.create_user(
        username='testuser',
        password='testpass123',
        is_staff=True,
        is_superuser=True  # This ensures full permissions
    )

@pytest.fixture
def authenticated_client(api_client, user):
    api_client.force_authenticate(user=user)
    return api_client

@pytest.fixture
def customer(user):
    return Customer.objects.create(
        user=user,
        phone='1234567890',  # Changed from phone_number to phone
        address='Test Address'
    )

@pytest.fixture
def category():
    return Category.objects.create(
        name='Test Category',
        slug='test-category',
        description='Test Description'
    )

@pytest.fixture
def product(category):
    return Product.objects.create(
        name='Test Product',
        slug='test-product',
        description='Test Description',
        price='99.99',
        category=category,
        stock=10,
        is_available=True
    )

@pytest.fixture
def order(customer, product):
    order = Order.objects.create(
        customer=customer,
        total_amount='99.99',
        shipping_address='123 Test St',
        shipping_city='Test City',
        shipping_country='Test Country',
        shipping_postal_code='12345'
    )
    OrderItem.objects.create(
        order=order,
        product=product,
        quantity=1,
        price='99.99'
    )
    return order

@pytest.fixture(autouse=True)
def cleanup_database():
    yield
    OrderItem.objects.all().delete()
    Order.objects.all().delete()
    Product.objects.all().delete()
    Category.objects.all().delete()
    Customer.objects.all().delete()
    User.objects.all().delete()
# savannah_app/tests/test_models.py
import pytest
from django.contrib.auth.models import User
from decimal import Decimal
from savannah_app.models import Category, Product, Customer, Order, OrderItem

@pytest.fixture
def user():
    return User.objects.create_user(
        username='testuser',
        email='test@example.com',
        password='testpass123'
    )

@pytest.fixture
def customer(user):
    return Customer.objects.create(
        user=user,
        phone='1234567890',
        address='123 Test St',
        city='Test City',
        country='Test Country',
        postal_code='12345'
    )

@pytest.fixture
def category():
    return Category.objects.create(
        name='Electronics',
        slug='electronics',
        description='Electronic products'
    )

@pytest.fixture
def product(category):
    return Product.objects.create(
        name='Test Product',
        slug='test-product',
        description='Test Description',
        price=Decimal('99.99'),
        category=category,
        stock=10
    )

@pytest.fixture
def order(customer):
    return Order.objects.create(
        customer=customer,
        total_amount=Decimal('99.99'),
        shipping_address='123 Test St',
        shipping_city='Test City',
        shipping_country='Test Country',
        shipping_postal_code='12345'
    )

@pytest.mark.django_db
class TestCategory:
    def test_create_category(self):
        category = Category.objects.create(
            name='Test Category',
            slug='test-category',
            description='Test Description'
        )
        assert category.name == 'Test Category'
        assert category.slug == 'test-category'
        assert str(category) == 'Test Category'

    def test_category_hierarchy(self):
        parent = Category.objects.create(name='Parent', slug='parent')
        child = Category.objects.create(name='Child', slug='child', parent=parent)
        assert child.parent == parent
        assert child in parent.children.all()

@pytest.mark.django_db
class TestProduct:
    def test_create_product(self, category):
        product = Product.objects.create(
            name='Test Product',
            slug='test-product',
            description='Test Description',
            price=Decimal('99.99'),
            category=category
        )
        assert product.name == 'Test Product'
        assert product.price == Decimal('99.99')
        assert str(product) == 'Test Product'

    def test_product_availability(self, product):
        assert product.is_available == True
        product.stock = 0
        product.save()
        assert product.is_available == True  # Still true as is_available is independent

@pytest.mark.django_db
class TestCustomer:
    def test_create_customer(self, user):
        customer = Customer.objects.create(
            user=user,
            phone='1234567890',
            address='123 Test St',
            city='Test City',
            country='Test Country',
            postal_code='12345'
        )
        assert customer.phone == '1234567890'
        assert str(customer) == f"{user.username} - 1234567890"

@pytest.mark.django_db
class TestOrder:
    def test_create_order(self, customer, product):
        order = Order.objects.create(
            customer=customer,
            total_amount=Decimal('99.99'),
            shipping_address='123 Test St',
            shipping_city='Test City',
            shipping_country='Test Country',
            shipping_postal_code='12345'
        )
        assert order.status == 'pending'
        assert order.order_number.startswith('ORD-')

    def test_order_items(self, order, product):
        order_item = OrderItem.objects.create(
            order=order,
            product=product,
            quantity=2,
            price=product.price
        )
        assert order_item.quantity == 2
        assert str(order_item).startswith('2x Test Product in Order #')

import pytest
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from decimal import Decimal
from savannah_app.tests.test_settings import mock_africastalking

@pytest.mark.django_db
class TestCategoryViewSet:
    def test_list_categories(self, authenticated_client, category):
        url = reverse('category-list')
        response = authenticated_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 1

    def test_create_category(self, authenticated_client):
        url = reverse('category-list')
        data = {
            'name': 'New Category',
            'slug': 'new-category',
            'description': 'New Description'
        }
        response = authenticated_client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['name'] == 'New Category'

    def test_average_price(self, authenticated_client, category, product):
        url = reverse('category-average-price', kwargs={'pk': category.pk})
        response = authenticated_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert Decimal(str(response.data['average_price'])) == Decimal('99.99')

@pytest.mark.django_db
class TestProductViewSet:
    def test_list_products(self, authenticated_client, product):
        url = reverse('product-list')
        response = authenticated_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 1

    def test_create_product(self, authenticated_client, category):
        url = reverse('product-list')
        data = {
            'name': 'New Product',
            'slug': 'new-product',
            'description': 'New Description',
            'price': '149.99',
            'category': category.id,
            'stock': 10,
            'is_available': True
        }
        response = authenticated_client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['name'] == 'New Product'


@pytest.mark.django_db
class TestOrderViewSet:
    def test_create_order(self, authenticated_client, customer, product, mock_africastalking):
        # Update customer with valid phone number
        customer.phone = "+254123456789"
        customer.save()
        
        url = reverse('order-list')
        data = {
            'customer': customer.id,
            'total_amount': '99.99',
            'shipping_address': '123 Test St',
            'shipping_city': 'Test City',
            'shipping_country': 'Test Country',
            'shipping_postal_code': '12345',
            'items': [{
                'product': product.id,
                'quantity': 1,
                'price': '99.99'
            }]
        }
        
        # Make the request
        response = authenticated_client.post(url, data, format='json')
        
        # Print debug information
        print(f"Response status: {response.status_code}")
        print(f"Response data: {response.data}")
        
        # Assertions
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['status'] == 'pending'
        
        # Verify that send_order_confirmation was called
        mock_africastalking['confirm'].assert_called_once()
        
        # If you want to verify the notification wasn't sent yet (since it's only for status updates)
        assert not mock_africastalking['notify'].called
        
        # Optional: Verify the specific confirmation call if needed
        call_args = mock_africastalking['confirm'].call_args
        if call_args is not None:
            args, kwargs = call_args
            print(f"Confirmation call args: {args}")
            print(f"Confirmation call kwargs: {kwargs}")
            
    
import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import Category, Product, Order

@pytest.mark.django_db
class TestCategory:
    def test_create_category(self, api_client):
        url = reverse('category-list')
        data = {'name': 'Test Category'}
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED
        assert Category.objects.count() == 1

@pytest.mark.django_db
class TestProduct:
    def test_create_product(self, api_client, category):
        url = reverse('product-list')
        data = {
            'name': 'Test Product',
            'description': 'Test Description',
            'price': '99.99',
            'category': category.id
        }
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED
        assert Product.objects.count() == 1
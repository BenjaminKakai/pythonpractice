# README.md
# Savannah E-commerce API

A Django REST API for an e-commerce platform.

## Setup

1. Clone the repository
2. Create virtual environment: `python -m venv venv`
3. Activate virtual environment: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Run migrations: `python manage.py migrate`
6. Create superuser: `python manage.py createsuperuser`
7. Run server: `python manage.py runserver`

## Features

- Product category management with hierarchical structure
- Product CRUD operations
- Order management with SMS notifications
- Admin email notifications
- OpenAPI documentation
- Containerized deployment
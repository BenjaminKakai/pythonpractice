# Savannah E-commerce API

A robust Django REST Framework API for an e-commerce platform featuring hierarchical product categories, order management, and automated notifications.

## Features

- **Authentication & Authorization**
  - JWT-based authentication
  - Token-based API access
  - Role-based permissions

- **Product Management**
  - Hierarchical category structure (unlimited depth)
  - Full CRUD operations for products
  - Category-based product organization
  - Price tracking and updates

- **Customer Management**
  - Customer profiles with contact information
  - Order history tracking
  - Address management

- **Order Processing**
  - Order creation and management
  - Multiple products per order
  - Order status tracking
  - Automated notifications

- **Notifications**
  - SMS notifications via Africa's Talking
  - Email notifications for administrators
  - Order status updates

## Technical Stack

- Django 4.x
- Django REST Framework
- PostgreSQL
- JWT Authentication
- Africa's Talking SMS Gateway
- Docker & Docker Compose

## Setup & Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd savannah-ecommerce
```

2. Set up the environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. Configure environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

4. Initialize the database:
```bash
python manage.py migrate
python manage.py createsuperuser
```

5. Run the development server:
```bash
python manage.py runserver
```

## API Endpoints

### Authentication
```
POST /api/token/ - Obtain JWT token
POST /api/token/refresh/ - Refresh JWT token
```

### Categories
```
GET /api/v1/categories/ - List all categories
POST /api/v1/categories/ - Create a category
GET /api/v1/categories/{id}/ - Retrieve category
PUT /api/v1/categories/{id}/ - Update category
DELETE /api/v1/categories/{id}/ - Delete category
GET /api/v1/categories/{id}/average_price/ - Get average price of products in category
```

### Products
```
GET /api/v1/products/ - List all products
POST /api/v1/products/ - Create a product
GET /api/v1/products/{id}/ - Retrieve product
PUT /api/v1/products/{id}/ - Update product
DELETE /api/v1/products/{id}/ - Delete product
```

### Customers
```
GET /api/v1/customers/ - List all customers
POST /api/v1/customers/ - Create a customer
GET /api/v1/customers/{id}/ - Retrieve customer
PUT /api/v1/customers/{id}/ - Update customer
DELETE /api/v1/customers/{id}/ - Delete customer
```

### Orders
```
GET /api/v1/orders/ - List all orders
POST /api/v1/orders/ - Create an order
GET /api/v1/orders/{id}/ - Retrieve order
PUT /api/v1/orders/{id}/ - Update order
DELETE /api/v1/orders/{id}/ - Delete order
```

## API Usage Examples

### Authentication
```bash
# Obtain token
curl -X POST http://localhost:8000/api/token/ \
     -H "Content-Type: application/json" \
     -d '{"username": "your_username", "password": "your_password"}'
```

### Creating a Product
```bash
curl -X POST http://localhost:8000/api/v1/products/ \
     -H "Authorization: Bearer your_access_token" \
     -H "Content-Type: application/json" \
     -d '{
         "name": "Product Name",
         "description": "Product Description",
         "price": "99.99",
         "category": 1
     }'
```

## Docker Deployment

1. Build the image:
```bash
docker-compose build
```

2. Run the containers:
```bash
docker-compose up -d
```

## Testing

Run the test suite:
```bash
python manage.py test
```

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.